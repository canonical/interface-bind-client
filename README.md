# Overview

This interface supports integration between designate-bind and prometheus-bind-exporter-operator.

# Usage

## Layer
To consume this interface in your charm or layer, add the following to `layer.yaml`:

```yaml
includes: ['interface:bind-client']
```

## Provides

Add a provides interface of type `bind-client` to your charm or layers
`metadata.yaml`:

```yaml
provides:
  dns-backend:
    interface: bind-rndc
  bind-stats:
    interface: bind-client
```

* Note that `charm-designate-bind` normally works with `charm-designate` with the `bind-rndc` interface.

### flag: {relation_name}.connected

This flag is set when the `bind-exporter` unit is joined and removes when departed, or broken.

For example, the following code is used in [charm-designate-bind](https://opendev.org/openstack/charm-designate-bind) and the charm may not use a `bind-exporter`. When the `bind-exporter` is not present, the flag `{relation_name}.connected` won't be set and the templates will react accordingly with this.

When the flag `{relation_name}.connected` is set, it will create a new file `/etc/bind/stats.conf` in charm-designate-bind with the following content:
```
statistics-channels {
  inet <stats-listen-net> port <stats-port> allow { <client-ip>; };
};
```
It will also include this new file at `etc/bind/named.conf`. This will open a statistics channel in bind that `bind-exporter`
can expose metrics to collect.

When the flag is not set, the statistics channel is closed.

If the `bind-exporter` is present in the bundle, it will check if configuration has changed and send this information through the endpoint of the relation.

```python
import charm.openstack.designate_bind as designate_bind

@reactive.when('rndckey.available')
@reactive.when('dns-backend.related')
def config_changed():
    '''Render configs and restart services if necessary.'''

    dns_backend_endpoint = reactive.endpoint_from_flag("dns-backend.related")
    bind_stats_endpoint = reactive.endpoint_from_name("bind-stats")

    if reactive.is_flag_set('bind-stats.connected'):
        config = hookenv.config()
        if config.changed("stats-port"):
            shared_data = {
                'stats-port': hookenv.config('stats-port'),
                'stats-ip': '127.0.0.1'
            }
            bind_stats_endpoint.configure(shared_data)

    designate_bind.set_apparmor()
    designate_bind.render_all_configs(
        [dns_backend_endpoint, bind_stats_endpoint]
    )
```

## Requires

Add a requires interface of type `bind-client` to your charm or layers
`metadata.yaml`:

```yaml
requires:
  bind-stats:
    interface: bind-client
```

### flag: {relation_name}.connected
This flag is set when the `bind-exporter` unit is joined and removes when departed, or broken.

```python
@reactive.when('bind-stats.connected')
def start_bind_exporter():

    bind_stats_endpoint = reactive.endpoint_from_flag("bind-stats")
    config = bind_stats_endpoint.get_config()
    # logic to start the bind exporter
```
