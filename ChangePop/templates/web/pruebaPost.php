
switch ($_SERVER['HTTP_ORIGIN']) {
    case 'http://kelpa-api.herokuapp.com/login': case 'http://kelpa-api.herokuapp.com/login':
    header('Access-Control-Allow-Origin: '.$_SERVER['HTTP_ORIGIN']);
    header('Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS');
    header('Access-Control-Max-Age: 1000');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
    break;
}