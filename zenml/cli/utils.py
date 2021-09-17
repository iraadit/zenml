#  Copyright (c) ZenML GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
import datetime
from datetime import timedelta
from typing import List, Any, Text, Dict

import click
from dateutil import tz


def title(text: Text):
    """Echo a title formatted string on the CLI.

    Args:
      text: Input text string.
    """
    click.echo(click.style(text.upper(), fg="cyan", bold=True, underline=True))


def confirmation(text: Text, *args, **kwargs) -> bool:
    """Echo a confirmation string on the CLI.

    Args:
      text: Input text string.
      *args: Args to be passed to click.confirm().
      **kwargs: Kwargs to be passed to click.confirm().

    Returns:
        Boolean based on user response.
    """
    return click.confirm(click.style(text, fg="yellow"), *args, **kwargs)


def question(text: Text, *args, **kwargs) -> Any:
    """Echo a question string on the CLI.

    Args:
      text: Input text string.
      *args: Args to be passed to click.prompt().
      **kwargs: Kwargs to be passed to click.prompt().

    Returns:
        The answer to the question of any type, usually string.
    """
    return click.prompt(text=text, *args, **kwargs)


def declare(text: Text):
    """Echo a declaration on the CLI.

    Args:
      text: Input text string.
    """
    click.echo(click.style(text, fg="green"))


def notice(text: Text):
    """Echo a notice string on the CLI.

    Args:
      text: Input text string.
    """
    click.echo(click.style(text, fg="cyan"))


def error(text: Text):
    """Echo an error string on the CLI.

    Args:
      text: Input text string.

    Raises:
        click.ClickException when called.
    """
    raise click.ClickException(message=click.style(text, fg="red", bold=True))


def warning(text: Text):
    """Echo a warning string on the CLI.

    Args:
      text: Input text string.
    """
    click.echo(click.style(text, fg="yellow", bold=True))


def pretty_print(obj: Any):
    """Pretty print an object on the CLI.

    Args:
      obj: Any object with a __str__ method defined.
    """
    click.echo(str(obj))


def format_date(
    dt: datetime.datetime, format: Text = "%Y-%m-%d %H:%M:%S"
) -> Text:
    """Format a date into a string.

    Args:
      dt: Datetime object to be formatted.
      format: The format in string you want the datetime formatted to.

    Returns:
        Formatted string according to specification.
    """
    if dt is None:
        return ""
    local_zone = tz.tzlocal()
    # make sure this is UTC
    dt = dt.replace(tzinfo=tz.tzutc())
    local_time = dt.astimezone(local_zone)
    return local_time.strftime(format)


def format_timedelta(td: timedelta) -> Text:
    """Format a timedelta into a string.

    Args:
      td: datetime.timedelta object to be formatted.

    Returns:
        Formatted string according to specification.
    """
    if td is None:
        return ""
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


def parse_unknown_options(args: List[Text]) -> Dict[Text]:
    """Parse unknown options from the cli.

    Args:
      args: A list of strings from the CLI.

    Returns:
        Dict of parsed args.
    """
    warning_message = (
        "Please provide args with a proper "
        "identifier as the key and the following structure: "
        '--custom_argument="value"'
    )

    assert all(a.startswith("--") for a in args), warning_message
    assert all(len(a.split("=")) == 2 for a in args), warning_message

    p_args = [a.lstrip("--").split("=") for a in args]

    assert all(k.isidentifier() for k, _ in p_args), warning_message

    r_args = {k: v for k, v in p_args}
    assert len(p_args) == len(r_args), "Replicated arguments!"

    return r_args
