# election
![GitHub](https://img.shields.io/github/license/yeonho1/election)

> Django를 활용한 선거 시스템

>  *  Features
>
>   * User authentication
>   * Voting
>   * Creation of Vote topic & Vote selection

## Usage

### Requirement Installation

먼저 다음이 필요합니다.

```
Python 3+
Django 3.0.5 (Recommended Version)
Markdown 3.2.2 (Recommended Version)
```

[Python 공식 페이지](https://python.org)에 가셔서 (또는 Unix의 경우 `apt`나 `yum` 등 패키지 관리자를 사용해서) Python 3 를 설치하신 뒤에, `pip`로 `django==3.0.5`와 `markdown==3.2.2`를 설치해주시면 됩니다.

#### 유닉스 기반 (Python 2 기본 설치된 경우)

```
$ pip3 install django==3.0.5
...
$ pip3 install markdown==3.2.2
```

**참고**: 경우에 따라 `sudo` 권한이 필요할 수도 있습니다.

#### Non-unix (Python 2가 설치되지 않은 경우)

```
$ pip install django==3.0.5
...
$ pip install markdown==3.2.2
```

**참고**: Python 2가 설치되어있지 않아도 `pip3`로 해야 할 수 있습니다. 만약에 되지 않으면 `pip3`로 시도해보세요.

### SECRET KEY Configuration

모두 설치하신 뒤에 [Django Secret Key Generator](https://miniwebtool.com/django-secret-key-generator/)에 가셔서 `SECRET_KEY`를 생성하신 다음, 환경 변수 `DJANGO_SECRET_KEY`로 지정해주십시오.

**또는**

`election/election/settings.py`의

```python
def get_secret_key(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "You must set the environment variable {}!".format(var_name)
        raise ImproperlyConfigured(error_msg)
SECRET_KEY = get_secret_key("DJANGO_SECRET_KEY")
```
이 부분을
```python
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
```
로 고치셔도 됩니다.

### Run server

보통 테스트할 때 처럼

```
$ python manage.py runserver [port]
```
와 같은 방식으로 실행해도 되지만, 실제로 사용하는 경우에는 Apache의 `mod_wsgi`와 연동하는 것을 추천드립니다.