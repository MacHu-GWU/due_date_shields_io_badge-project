# -*- coding: utf-8 -*-

from chalice import Chalice
from datetime import datetime, timedelta
from dateutil.parser import parse


def find_label_message_color(due_date: datetime, period_in_sec: int):
    due_date = due_date.replace(hour=23, minute=59, second=59)
    now = datetime.utcnow()
    first_third = due_date - timedelta(seconds=int(period_in_sec * 2 / 3))
    second_third = due_date - timedelta(seconds=int(period_in_sec * 1 / 3))

    date_message = str(due_date.date())
    time_left_in_sec = (due_date - now).total_seconds()
    if time_left_in_sec > 365 * 24 * 3600:
        how_long_left = "in {:.1f} years".format(time_left_in_sec / (365 * 24 * 3600))
    elif time_left_in_sec > 30 * 24 * 3600:
        how_long_left = "in {:.1f} months".format(time_left_in_sec / (30 * 24 * 3600))
    elif time_left_in_sec > 7 * 24 * 3600:
        how_long_left = "in {:.1f} weeks".format(time_left_in_sec / (7 * 24 * 3600))
    elif time_left_in_sec > 24 * 3600:
        how_long_left = "in {:.1f} days".format(time_left_in_sec / (24 * 3600))
    elif time_left_in_sec > 0:
        how_long_left = "in {:.1f} hours".format(time_left_in_sec / 3600)
    else:
        how_long_left = "OVERDUE"

    if now < first_third:
        color = "brightgreen"
    elif now < second_third:
        color = "yellow"
    elif now < due_date:
        color = "orange"
    else:
        color = "red"
    label = "due"
    message = f"{date_message} | {how_long_left}"
    return label, message, color


def build_response(due_date: str, period_in_sec: int):
    try:
        label, message, color = find_label_message_color(parse(due_date), period_in_sec)
        return {
            "schemaVersion": 1,
            "label": label,
            "message": message,
            "color": color,
        }
    except Exception as e:
        return {
            "schemaVersion": 1,
            "label": "error",
            "message": str(e),
            "color": "lightgrey",
        }


app = Chalice(app_name="due_date_shields_io_badge")


@app.route("/1d/{due_date}")
def handler_one_day(due_date):
    return build_response(due_date, 1 * 24 * 3600)


@app.route("/3d/{due_date}")
def handler_three_days(due_date):
    return build_response(due_date, 3 * 24 * 3600)


@app.route("/1w/{due_date}")
def handler_one_week(due_date):
    return build_response(due_date, 1 * 7 * 24 * 3600)


@app.route("/2w/{due_date}")
def handler_two_weeks(due_date):
    return build_response(due_date, 2 * 7 * 24 * 3600)


@app.route("/1m/{due_date}")
def handler_one_month(due_date):
    return build_response(due_date, 1 * 30 * 24 * 3600)


@app.route("/2m/{due_date}")
def handler_two_month(due_date):
    return build_response(due_date, 2 * 30 * 24 * 3600)


@app.route("/3m/{due_date}")
def handler_three_months(due_date):
    return build_response(due_date, 3 * 30 * 24 * 3600)


if __name__ == "__main__":
    print(build_response("2021-08-13", 14 * 24 * 3600))
