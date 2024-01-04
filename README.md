# weewx-healthchecks

A WeeWX extension that uses [Healthchecks.io](https://healthchecks.io) to monitor WeeWX.

At WeeWX startup, a [start signal](https://healthchecks.io/docs/http_api/#start-uuid) is sent to Healthchecks.io.

When WeeWX shutsdown, a [failure signal](https://healthchecks.io/docs/http_api/#fail-uuid) is sent to Healthchecks.io.

Every WeeWX report cycle, a [success signal](https://healthchecks.io/docs/http_api/#success-uuid) is sent to Healthchecks.io.

How to handle missing or late `success signals` can be [configured](https://healthchecks.io/docs/configuring_checks/) at [Healthchecks.io](https://healthchecks.io).

The method(s) of notification are also [selected](https://healthchecks.io/docs/configuring_notifications/) at [Healthchecks.io](https://healthchecks.io).

The [getting started](https://healthchecks.io/docs/) is a good introduction.

## Installation and configuring `weewx-healthchecks`

After installing `weewx-healthchecks`, edit `weewx.conf`
In the

```text
[StdReport]
    [Healthchecks]
```

1. Set `enable = true`
2. Set `uuid` to the `uuid` that is associated with the `check` created at Healthchecks.io.

Restart WeeWx
