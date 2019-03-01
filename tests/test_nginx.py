import os
import shutil

import pytest
import requests

from pytest_nginx import factories


@pytest.fixture(scope="session")
def nginx_server_root(tmpdir_factory):
    return tmpdir_factory.mktemp("nginx-server-root")


nginx_proc = factories.nginx_proc("nginx_server_root")


@pytest.fixture(scope="module")
def nginx_hello_world(nginx_proc):
    f = open(os.path.join(nginx_proc.server_root, "index.html"), "w")
    f.write("Hello world! This is pytest-nginx.")
    f.close()
    return nginx_proc


def test_hello_world(nginx_hello_world):
    url = "http://{}:{}".format(nginx_hello_world.host, nginx_hello_world.port)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == "Hello world! This is pytest-nginx."


nginx_php_proc = factories.nginx_php_proc("nginx_server_root")


@pytest.fixture(scope="module")
def nginx_php_hello_world(nginx_php_proc):
    f = open(os.path.join(nginx_php_proc.server_root, "index.php"), "w")
    f.write("<?php\nprint('Hello world! This is pytest-nginx, serving PHP!')\n?>")
    f.close()
    return nginx_php_proc


def find_executable(n):
    try:
        shutil.which(n)
        return True
    except shutil.Error:
        return None


@pytest.mark.skipif(not find_executable("php-fpm"),
                    reason="php-fpm not found in path")
def test_php_hello_world(nginx_php_hello_world):
    url = "http://{}:{}".format(nginx_php_hello_world.host, nginx_php_hello_world.port)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == "Hello world! This is pytest-nginx, serving PHP!"


nginx_bad_config_proc = factories.nginx_proc("nginx_server_root", config_template=__file__)


def test_borked_config(request):
    with pytest.raises(RuntimeError):
        request.getfixturevalue("nginx_bad_config_proc")


extra_params_template_path = os.path.join(
    os.path.dirname(__file__), "extra_params_template")

nginx_template_extra_proc = factories.nginx_proc(
    "nginx_server_root",
    config_template=extra_params_template_path,
    template_extra_params={"extra": "123"})


@pytest.fixture(scope="module")
def nginx_template_extra(nginx_template_extra_proc):
    f = open(os.path.join(nginx_template_extra_proc.server_root, "123.html"), "w")
    f.write("Hello world! This is pytest-nginx.")
    f.close()
    return nginx_template_extra_proc


def test_template_extra_params(nginx_template_extra):
    url = "http://{}:{}".format(nginx_template_extra.host, nginx_template_extra.port)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == "Hello world! This is pytest-nginx."
