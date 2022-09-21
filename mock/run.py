"""
    mock script
"""

if __name__ == "__main__":
    from env_wrapper import load_env
    load_env()
    from mock.mock import Mock
    Mock.clean_db()
    Mock.setup_db()
    Mock.mock()
