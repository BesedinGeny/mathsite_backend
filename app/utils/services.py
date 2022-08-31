from typing import Any, List, Optional, Type

from fastapi import Request
from pydantic import BaseModel
from user_agents import parse

from app import models


def user_agent_parser(user_agent: str, request: Request):
    """
    Вспомогательная функция для получения устройства, ос пользователя и ip.
    
    :param user_agent: данные из user-agent
    :param request: данные из запроса
    """
    ip_address = request.scope.get('root_path')
    agent_from_user = f'{request.headers.get("Agent", "")}/ '
    platform_from_user = f'{request.headers.get("platform", "")}/ '
    user_agent_data = parse(user_agent)
    agent = (f'{agent_from_user}{user_agent_data.browser[0]}'
             f'{user_agent_data.browser[2]}')
    platform = (f'{platform_from_user}{user_agent_data.device[0]}',
                f' {user_agent_data.os[0]}{user_agent_data.os[2]}')
    return agent, platform, ip_address


def deep_translate_to_locale(
        model: Any,
        locale: Optional[str],
        output_schema: Type[BaseModel]
) -> BaseModel:
    """
    Переводит все возможные свойства на выбранный язык.
    Перед вызовом этой функции надо вызвать check_locale, чтобы избежать не локализованных
    объектов
    
    :param model: объект sqlalchemy модели
    :param locale: строка, соответсвующая языку или None
    :param output_schema: класс pydantic схемы, который нужно вернуть, должно быть orm_mode = True
    """
    response_schema = output_schema.from_orm(model)
    if locale:
        if hasattr(model, 'title_locales'):
            for locale_obj in model.title_locales:
                if locale_obj.locale == locale:
                    response_schema.title_locales = [locale_obj]
                    break
        
        if hasattr(model, 'description_locales'):
            for locale_obj in model.description_locales:
                if locale_obj.locale == locale:
                    response_schema.description_locales = [locale_obj]
                    break
        
        if hasattr(model, 'text_locales'):
            for locale_obj in model.text_locales:
                if locale_obj.locale == locale:
                    response_schema.text_locales = [locale_obj]
                    break
        
        if hasattr(model, 'assistances'):
            assistance_list = []
            for assistance in model.assistances:
                for locale_obj in assistance.text_locales:
                    if locale_obj.locale == locale:
                        assistance.text_locales = [locale_obj]
                        assistance_list.append(assistance)
                        break
            response_schema.assistances = assistance_list
        
        if hasattr(model, 'tags'):
            tag_list = []
            for tag in model.tags:
                for locale_obj in tag.text_locales:
                    if locale_obj.locale == locale:
                        tag.text_locales = [locale_obj]
                        tag_list.append(tag)
                        break
            response_schema.tags = tag_list
            
        if hasattr(model, 'buttons'):
            button_list = []
            for button in model.buttons:
                for locale_obj in button.text_locales:
                    if locale_obj.locale == locale:
                        button.text_locales = [locale_obj]
                        button_list.append(button)
                        break
            response_schema.buttons = button_list
    return response_schema


def check_locale(query: Any, locale: Optional[str], instrumented_list: List):
    """
    Возвращает квери с проверкой основного списка локализованных полей (title/description/text)
    на наличие нужного языка
    
    :param query: sqlalchemy-query объект
    :param locale: строка, соответсвующая языку или None
    :param instrumented_list: список локализацций у объекта, relationship(uselist=True)
    :return: sqlalchemy-query объект
    """
    if locale:
        query = query.where(
            instrumented_list.any(models.Locale.locale == locale))  # noqa
    return query
