err_bad_request = (
    "HTTP/1.1 400 BAD REQUEST\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>400 Bad Request</h1>
</html>
    """
).encode('utf-8')

err_forbidden = (
    "HTTP/1.1 403 FORBIDDEN\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>403 Forbidden</h1>
</html>
    """
).encode('utf-8')

err_page_nf = (
    "HTTP/1.1 404 PAGE NOT FOUND\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>404 Page Not Found</h1>
</html>
    """
).encode('utf-8')

err_internal_error = (
    "HTTP/1.1 500 INTERNAL ERROR\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>500 Internal Error</h1>
</html>
    """
).encode('utf-8')

err_not_implemented = (
    "HTTP/1.1 501 NOT IMPLEMENTED\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>501 Not Implemented</h1>
</html>
    """
).encode('utf-8')