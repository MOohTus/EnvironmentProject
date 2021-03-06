#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Morgane T.

Custom click class to add some functionalities.
"""

import click

# From : https://stackoverflow.com/questions/44247099/click-command-line-interfaces-make-options-required-if-other-optional-option-is


class RequiredIf(click.Option):
    """
    Add new parameter : RequiredIf
    Check if two parameters are given together.
    """
    def __init__(self, *args, **kwargs):
        self.required_if = kwargs.pop('required_if')
        assert self.required_if, "'required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') +
                          'NOTE: This argument is required if %s chosen.' %
                          self.required_if
                          ).strip()
        super(RequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.required_if in opts:
            if self.name not in opts:
                raise click.UsageError(
                    "Illegal usage: `{}` is required with "
                    "`{}`.".format(
                        self.name,
                        self.required_if
                    )
                )
        return super(RequiredIf, self).handle_parse_result(ctx, opts, args)
