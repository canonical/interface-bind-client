# Overview

This interface supports integration between designate-bind and prometheus-bind-exporter-operator.

# Usage

## metadata
To consume this interface in your charm or layer, add the following to `layer.yaml`:

```yaml
includes: ['interface:bind-client']
```

and add a requires interface of type `bind-client` to your charm or layers
`metadata.yaml`:

```yaml
requires:
  bind-stats:
    interface: bind-client
```

## flag: {relation_name}.connected

This flag is set when the subordinate unit is joined and removes when departed.

For example, the following code will update the relation just when the relation is estabilished and the configuration changed:

```python
@reactive.when('rndckey.available')
@reactive.when('dns-backend.related')
def config_changed():
    '''Render configs and restart services if necessary'''
    endpoints = [
        reactive.endpoint_from_flag('dns-backend.related'),
        reactive.endpoint_from_name('bind-stats')
    ]

    if reactive.is_flag_set('bind-stats.connected'):
        config = hookenv.config()
        if config.changed("stats-port"):
            endpoints[1].configure(hookenv.config('stats-port'))

    designate_bind.set_apparmor()
    designate_bind.render_all_configs(endpoints)
```
When this flag is set, it will create a new file `/etc/bind/stats.conf` in charm-designate-bind with the following content:
```
statistics-channels {
  inet <stats-listen-net> port <stats-port> allow { <client-ip>; };
};
```
It will also include this new file at `etc/bind/named.conf`. This will open a statistics channel in bind that prometheus-bind-exporter
can expose metrics for prometheus to collect.

When the flag is not set, the statistics channel is closed.