"""
    settings service
"""
from database.database import db_session

from settings.model import Setting


class SettingService:
    @staticmethod
    def set_settings(settings: Setting):
        try:
            original = SettingService.get_settings()

            if original is None:
                db_session.add(settings)
            else:
                original.charge_within_hour = settings.charge_within_hour
                original.charge_more_than_a_hour = settings.charge_more_than_a_hour
                original.charge_more_than_a_day = settings.charge_more_than_a_day

            db_session.commit()
            return settings
        except Exception as err:
            db_session.rollback()
            raise err

    @staticmethod
    def get_settings() -> Setting:
        return Setting.query.first()
