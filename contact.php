<?php
/**
 * Contact form handler.
 *
 * Sends two emails on each submission:
 *   1. the enquiry itself to the practice, always in Spanish
 *   2. an acknowledgement to the patient, in the language of the page they used
 *
 * Requires nothing beyond PHP's mail() (available on standard cPanel hosting).
 */

declare(strict_types=1);

const PRACTICE_EMAIL = 'info@drfabiodangelo.com';
const FROM_EMAIL     = 'info@drfabiodangelo.com';
const FROM_NAME      = "Dr. Fabio D'Angelo";

header('Content-Type: application/json; charset=utf-8');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'method_not_allowed']);
    exit;
}

/** Strip CR/LF so user input can never inject extra mail headers. */
function clean(string $value, int $maxLength = 200): string
{
    $value = str_replace(["\r", "\n", "\0"], ' ', $value);
    $value = trim($value);
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $maxLength);
    }
    return substr($value, 0, $maxLength);
}

$name    = clean((string)($_POST['name'] ?? ''), 120);
$email   = clean((string)($_POST['email'] ?? ''), 180);
$phone   = clean((string)($_POST['phone'] ?? ''), 60);
$lang    = strtolower(clean((string)($_POST['lang'] ?? 'es'), 5));
$honey   = trim((string)($_POST['website'] ?? ''));

// Message keeps its line breaks — it is only ever used in the body.
$message = trim(str_replace(["\r\n", "\r"], "\n", (string)($_POST['message'] ?? '')));
if (function_exists('mb_substr')) {
    $message = mb_substr($message, 0, 5000);
} else {
    $message = substr($message, 0, 5000);
}

// Bots fill hidden fields; humans never see this one.
if ($honey !== '') {
    echo json_encode(['ok' => true]);
    exit;
}

if ($name === '' || $email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'invalid_input']);
    exit;
}

if (!in_array($lang, ['es', 'en', 'fr'], true)) {
    $lang = 'es';
}

$langNames = ['es' => 'Español', 'en' => 'Inglés', 'fr' => 'Francés'];

/* ---------------------------------------------------------------- *
 * 1. Enquiry to the practice — always Spanish, whatever the visitor  *
 * ---------------------------------------------------------------- */

$adminSubject = 'Nueva solicitud de cita — ' . $name;

$adminBody = "Nueva solicitud recibida desde el formulario de contacto de la web.\n\n"
    . "Nombre:   {$name}\n"
    . "Email:    {$email}\n"
    . "Teléfono: " . ($phone !== '' ? $phone : '—') . "\n"
    . "Idioma:   " . $langNames[$lang] . "\n"
    . "Fecha:    " . date('d/m/Y H:i') . "\n\n"
    . "Mensaje:\n"
    . ($message !== '' ? $message : '(sin mensaje)') . "\n\n"
    . "----\n"
    . "Puedes responder directamente a este correo para contactar con el paciente.\n";

$adminHeaders = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'From: ' . mb_encode_mimeheader(FROM_NAME, 'UTF-8') . ' <' . FROM_EMAIL . '>',
    'Reply-To: ' . mb_encode_mimeheader($name, 'UTF-8') . ' <' . $email . '>',
];

$adminSent = mail(
    PRACTICE_EMAIL,
    mb_encode_mimeheader($adminSubject, 'UTF-8'),
    $adminBody,
    implode("\r\n", $adminHeaders),
    '-f' . FROM_EMAIL
);

/* ---------------------------------------------------------------- *
 * 2. Acknowledgement to the patient — in the language of the page    *
 * ---------------------------------------------------------------- */

$replies = [
    'es' => [
        'subject' => 'Gracias por contactar con el Dr. Fabio D\'Angelo',
        'body' => "Hola {$name}:\n\n"
            . "Gracias por ponerte en contacto con la consulta del Dr. Fabio D'Angelo.\n\n"
            . "Hemos recibido tu solicitud y nuestro equipo se pondrá en contacto contigo "
            . "lo antes posible para confirmar los detalles de tu cita.\n\n"
            . "Resumen de tu solicitud:\n"
            . "Nombre:   {$name}\n"
            . "Email:    {$email}\n"
            . "Teléfono: " . ($phone !== '' ? $phone : '—') . "\n"
            . ($message !== '' ? "\nMensaje:\n{$message}\n" : '')
            . "\nSi tu consulta es urgente, puedes llamarnos al +34 628 77 70 39.\n\n"
            . "Un cordial saludo,\n"
            . "Equipo del Dr. Fabio D'Angelo\n"
            . "Cirujano de Pie y Tobillo\n"
            . "Carrer de Pere II de Montcada, 16 · 08034 Barcelona\n"
            . "info@drfabiodangelo.com · +34 628 77 70 39\n",
    ],
    'en' => [
        'subject' => 'Thank you for contacting Dr. Fabio D\'Angelo',
        'body' => "Dear {$name},\n\n"
            . "Thank you for contacting the practice of Dr. Fabio D'Angelo.\n\n"
            . "We have received your request and our team will get back to you as soon as "
            . "possible to confirm the details of your appointment.\n\n"
            . "Summary of your request:\n"
            . "Name:   {$name}\n"
            . "Email:  {$email}\n"
            . "Phone:  " . ($phone !== '' ? $phone : '—') . "\n"
            . ($message !== '' ? "\nMessage:\n{$message}\n" : '')
            . "\nIf your enquiry is urgent, you can call us on +34 628 77 70 39.\n\n"
            . "Kind regards,\n"
            . "The team of Dr. Fabio D'Angelo\n"
            . "Foot & Ankle Surgeon\n"
            . "Carrer de Pere II de Montcada, 16 · 08034 Barcelona\n"
            . "info@drfabiodangelo.com · +34 628 77 70 39\n",
    ],
    'fr' => [
        'subject' => 'Merci d\'avoir contacté le Dr Fabio D\'Angelo',
        'body' => "Bonjour {$name},\n\n"
            . "Merci d'avoir contacté le cabinet du Dr Fabio D'Angelo.\n\n"
            . "Nous avons bien reçu votre demande et notre équipe vous recontactera dans les "
            . "meilleurs délais afin de confirmer les détails de votre rendez-vous.\n\n"
            . "Récapitulatif de votre demande :\n"
            . "Nom :       {$name}\n"
            . "E-mail :    {$email}\n"
            . "Téléphone : " . ($phone !== '' ? $phone : '—') . "\n"
            . ($message !== '' ? "\nMessage :\n{$message}\n" : '')
            . "\nSi votre demande est urgente, vous pouvez nous appeler au +34 628 77 70 39.\n\n"
            . "Cordialement,\n"
            . "L'équipe du Dr Fabio D'Angelo\n"
            . "Chirurgien du Pied et de la Cheville\n"
            . "Carrer de Pere II de Montcada, 16 · 08034 Barcelone\n"
            . "info@drfabiodangelo.com · +34 628 77 70 39\n",
    ],
];

$reply = $replies[$lang];

$patientHeaders = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'From: ' . mb_encode_mimeheader(FROM_NAME, 'UTF-8') . ' <' . FROM_EMAIL . '>',
    'Reply-To: ' . PRACTICE_EMAIL,
];

mail(
    $email,
    mb_encode_mimeheader($reply['subject'], 'UTF-8'),
    $reply['body'],
    implode("\r\n", $patientHeaders),
    '-f' . FROM_EMAIL
);

// The acknowledgement is a courtesy — only the practice copy decides success.
if (!$adminSent) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'send_failed']);
    exit;
}

echo json_encode(['ok' => true]);
