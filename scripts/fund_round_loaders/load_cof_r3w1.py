# flake8: noqa
from config.fund_loader_config.cof.cof_r3 import APPLICATION_BASE_PATH_COF_R3_W1
from config.fund_loader_config.cof.cof_r3 import ASSESSMENT_BASE_PATH_COF_R3_W1
from config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_1_ID
from config.fund_loader_config.cof.cof_r3 import cof_r3_sections
from config.fund_loader_config.cof.cof_r3 import fund_config
from config.fund_loader_config.cof.cof_r3 import round_config
from db.queries import insert_assessment_sections
from db.queries import insert_base_sections
from db.queries import insert_fund_data
from db.queries import insert_or_update_application_sections
from db.queries import upsert_round_data


def main() -> None:
    print("Inserting fund and round data.")
    insert_fund_data(fund_config)
    upsert_round_data(round_config)

    print("Inserting base sections config.")
    insert_base_sections(
        APPLICATION_BASE_PATH_COF_R3_W1,
        ASSESSMENT_BASE_PATH_COF_R3_W1,
        COF_ROUND_3_WINDOW_1_ID,
    )
    print("Inserting sections.")
    insert_or_update_application_sections(COF_ROUND_3_WINDOW_1_ID, cof_r3_sections)


if __name__ == "__main__":
    from app import app

    with app.app.app_context():
        main()
