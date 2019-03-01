NGINX_DEFAULT_CONFIG_TEMPLATE = """\
# nginx has to start in foreground, otherwise pytest-nginx won't be able to kill it
daemon off;
pid %TMPDIR%/nginx.pid;
error_log %TMPDIR%/error.log;
worker_processes auto;
worker_cpu_affinity auto;

events {
    worker_connections  1024;
}

http {
    default_type  application/octet-stream;
    access_log off;
    sendfile on;
    charset utf-8;

    server {
        listen       %PORT%;
        server_name  %HOST%;
        index  index.html index.htm;
        location / {
            root "%SERVER_ROOT%";
        }
    }
}
"""

NGINX_DEFAULT_PHP_CONFIG_TEMPLATE = """\
# nginx has to start in foreground, otherwise pytest-nginx won't be able to kill it
daemon off;
pid %TMPDIR%/nginx.pid;
error_log %TMPDIR%/error.log;
worker_processes auto;
worker_cpu_affinity auto;

events {
    worker_connections  1024;
}

http {
    default_type  application/octet-stream;
    access_log off;
    sendfile on;
    charset utf-8;

    server {
        listen       %PORT%;
        server_name  %HOST%;
        index  index.php;
        root "%SERVER_ROOT%";

        location ~ \.php$ {
            try_files $uri $document_root$fastcgi_script_name =404;
            fastcgi_pass unix:%PHP_FPM_SOCKET%;
            fastcgi_index index.php;

            fastcgi_param  SCRIPT_FILENAME    $document_root$fastcgi_script_name;
            fastcgi_param  QUERY_STRING       $query_string;
            fastcgi_param  REQUEST_METHOD     $request_method;
            fastcgi_param  CONTENT_TYPE       $content_type;
            fastcgi_param  CONTENT_LENGTH     $content_length;

            fastcgi_param  SCRIPT_NAME        $fastcgi_script_name;
            fastcgi_param  REQUEST_URI        $request_uri;
            fastcgi_param  DOCUMENT_URI       $document_uri;
            fastcgi_param  DOCUMENT_ROOT      $document_root;
            fastcgi_param  SERVER_PROTOCOL    $server_protocol;
            fastcgi_param  REQUEST_SCHEME     $scheme;
            fastcgi_param  HTTPS              $https if_not_empty;

            fastcgi_param  GATEWAY_INTERFACE  CGI/1.1;
            fastcgi_param  SERVER_SOFTWARE    nginx/$nginx_version;

            fastcgi_param  REMOTE_ADDR        $remote_addr;
            fastcgi_param  REMOTE_PORT        $remote_port;
            fastcgi_param  SERVER_ADDR        $server_addr;
            fastcgi_param  SERVER_PORT        $server_port;
            fastcgi_param  SERVER_NAME        $server_name;

            # PHP only, required if PHP was built with --enable-force-cgi-redirect
            fastcgi_param  REDIRECT_STATUS    200;
        }
    }
}
"""

PHP_FPM_DEFAULT_CONFIG_TEMPLATE = """\
[global]
error_log = %PHP_FPM_ERROR_LOG%

[www]
user = %PHP_FPM_USER%

listen = %PHP_FPM_SOCKET%

pm = dynamic
pm.max_children = 5
pm.min_spare_servers = 1
pm.max_spare_servers = 3
"""
