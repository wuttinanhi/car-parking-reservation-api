"""
    settings service
"""
from database.database import db_session
from werkzeug.exceptions import NotFound

from settings.model import Setting


class SettingService:
    @staticmethod
    def set_settings(settings: Setting):
        try:
            get_settings = SettingService.get_settings()
            Setting.query.filter(Setting.id == get_settings.id).update({
                "charge_within_hour": settings.charge_within_hour,
                "charge_more_than_a_hour": settings.charge_more_than_a_hour,
                "charge_more_than_a_day": settings.charge_more_than_a_day
            })
            db_session.commit()
            return settings
        except NotFound as err:
            db_session.add(settings)
            db_session.commit()
            return settings
        except Exception as err:
            db_session.rollback()
            raise err

    @staticmethod
    def get_settings() -> Setting:
        settings = Setting.query.first()
        if settings is None:
            raise NotFound("Settings not found!")
        return settings
