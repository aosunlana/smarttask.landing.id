<?php
/**
 * SmartTasker Indonesia — Brevo proxy (PHP, for shared hosting)
 * ==============================================================
 * Same job as worker.js / api/brevo.js but runs on any shared host with PHP.
 *
 * Setup:
 *   1. Put the API key in a file OUTSIDE the web root, e.g.
 *      /home/<account>/brevo-key.php  containing:
 *          <?php define('BREVO_API_KEY', 'xkeysib-...');
 *      and adjust the require path below.
 *      (Fallback: define the key directly in this file — acceptable since PHP
 *      source is never served, but outside-webroot is safer against
 *      misconfiguration.)
 *   2. Upload this file to public_html/brevo-proxy.php
 *   3. In js/brevo-config.js set:  PROXY_URL: '/brevo-proxy.php'
 */

// ── Configuration ─────────────────────────────────────────────
$keyFile = dirname(__DIR__, 1) . '/../brevo-key.php'; // adjust to your host's path
if (file_exists($keyFile)) {
    require $keyFile;
}
if (!defined('BREVO_API_KEY')) {
    // Fallback: uncomment and set directly (keep this file out of git!)
    // define('BREVO_API_KEY', 'xkeysib-XXXXXXXX');
}

// Tighten to 'https://smarttasker.id' before launch:
$allowedOrigin = '*';

// ── CORS / method handling ────────────────────────────────────
header('Access-Control-Allow-Origin: ' . $allowedOrigin);
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}
if (!defined('BREVO_API_KEY')) {
    http_response_code(500);
    echo json_encode(['error' => 'BREVO_API_KEY not configured']);
    exit;
}

// ── Validate payload ──────────────────────────────────────────
$payload = json_decode(file_get_contents('php://input'), true);
if (!is_array($payload) || empty($payload['email']) || !filter_var($payload['email'], FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['error' => 'Valid email required']);
    exit;
}

$allowedAttrs = ['FULLNAME', 'WHATSAPP', 'LOCATION', 'ROLE', 'TRADE_CATEGORY', 'LANGUAGE', 'GIVEAWAY_ENTRY'];
$attributes = [];
if (isset($payload['attributes']) && is_array($payload['attributes'])) {
    foreach ($allowedAttrs as $attr) {
        if (isset($payload['attributes'][$attr]) && is_string($payload['attributes'][$attr]) && strlen($payload['attributes'][$attr]) <= 500) {
            $attributes[$attr] = $payload['attributes'][$attr];
        }
    }
}

$listIds = [];
if (isset($payload['listIds']) && is_array($payload['listIds'])) {
    foreach ($payload['listIds'] as $id) {
        if (is_int($id) && $id > 0) {
            $listIds[] = $id;
        }
    }
}

// ── Forward to Brevo ──────────────────────────────────────────
$body = json_encode([
    'email'         => $payload['email'],
    'updateEnabled' => true,
    'listIds'       => $listIds,
    'attributes'    => (object) $attributes,
]);

$ch = curl_init('https://api.brevo.com/v3/contacts');
curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $body,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 15,
    CURLOPT_HTTPHEADER     => [
        'Content-Type: application/json',
        'api-key: ' . BREVO_API_KEY,
    ],
]);
$response = curl_exec($ch);
$status   = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

if ($status === 201 || $status === 204) {
    echo json_encode(['success' => true]);
    exit;
}

$decoded = json_decode((string) $response, true);
if (isset($decoded['code']) && $decoded['code'] === 'duplicate_parameter') {
    echo json_encode(['success' => true, 'duplicate' => true]);
    exit;
}

error_log('Brevo error ' . $status . ': ' . $response);
http_response_code(502);
echo json_encode(['error' => 'Brevo rejected the submission']);
