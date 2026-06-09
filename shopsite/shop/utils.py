import dns.exception
import dns.resolver
from django.core.validators import validate_email
from rest_framework.exceptions import ValidationError

# Частые опечатки доменов почтовых сервисов
KNOWN_TYPOS = {
    'gmail.co': 'gmail.com',
    'gmal.com': 'gmail.com',
    'gmial.com': 'gmail.com',
    'gamil.com': 'gmail.com',
    'yandex.co': 'yandex.ru',
    'yande.ru': 'yandex.ru',
    'mail.co': 'mail.ru',
    'mai.ru': 'mail.ru',
    'outlok.com': 'outlook.com',
    'hotmal.com': 'hotmail.com',
}


def validate_email_full(email):
    """Strict email validation — format + MX record check + typo check."""
    try:
        validate_email(email)
    except ValidationError:
        return False, 'Некорректный формат email.'

    domain = email.rsplit('@', 1)[1].lower()

    if domain in KNOWN_TYPOS:
        return False, f'Возможно, вы имели в виду {KNOWN_TYPOS[domain]}? Исправьте адрес.'

    try:
        dns.resolver.resolve(domain, 'MX', lifetime=3)
        return True, None
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return False, f'Домен {domain} не принимает почту. Проверьте адрес.'
