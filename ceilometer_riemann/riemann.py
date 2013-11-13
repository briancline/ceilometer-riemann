# -*- encoding: utf-8 -*-
#
# Copyright © 2013 SoftLayer Technologies, an IBM company
#
# Author: Brian Cline <bcline@softlayer.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Publish a sample encapsulated in Protocol Buffers to Riemann
"""

from ceilometer import publisher
from ceilometer.openstack.common import log
from ceilometer.openstack.common import network_utils
from ceilometer.openstack.common.gettextutils import _
import urlparse
import bernhard
import time
from oslo.config import cfg


LOG = log.getLogger(__name__)

METER_PUBLISH_OPTS = [
    cfg.StrOpt('port',
               default=5555,
               help='The default port on which Riemann listens',
               ),
    cfg.StrOpt('transport',
               default='udp',
               help='The default transport over which events should be sent '
                    'to a Riemann server (tcp or udp)',
               ),
    cfg.StrOpt('default_ttl',
               default=86400,
               help='The default amount of time in seconds that events sent '
                    'to Riemann are retained in its index. Any event that '
                    'passes through Ceilometer with a metadata attribute '
                    'of "ttl" will override this value.')
]


def register_opts(config):
    """Register the options for publishing metering messages to Riemann.
    """
    config.register_opts(METER_PUBLISH_OPTS, group='publisher_riemann')


register_opts(cfg.CONF)


def transport_class_from_str(transport_name):
    transports = {
        'tcp': bernhard.TCPTransport,
        'udp': bernhard.UDPTransport,
        # 'ssl': bernhard.SSLTransport
    }

    if transport_name not in transports:
        raise ValueError(_('Invalid transport type %(type)s' %
                         {'type': transport_name}))

    return transports.get(transport_name)


class RiemannPublisher(publisher.PublisherBase):

    def __init__(self, parsed_url):
        """Stuff!
        """

        LOG.info('RiemannPublisher.init')

        options = urlparse.parse_qs(parsed_url.query)

        self.transport = options.get('transport',
                                     cfg.CONF.publisher_riemann.transport)
        if not isinstance(self.transport, basestring):
            self.transport = self.transport.pop()

        transport_class = transport_class_from_str(self.transport)

        self.host, self.port = network_utils.parse_host_port(
            parsed_url.netloc,
            default_port=cfg.CONF.publisher_riemann.port)

        self.client = bernhard.Client(host=self.host, port=self.port,
                                      transport=transport_class)

    def publish_samples(self, context, samples):
        """Send a metering message for publishing

        :param context: Execution context from the service or RPC call
        :param samples: Samples from pipeline after transformation
        """

        # TODO: move attributes construction to helper method
        ignore_metadata_keys = ['host', 'ttl']

        try:
            if not self.client.connection:
                self.client.connect()
        except Exception as e:
            LOG.warn(_('Unable to connect: %(exception)s') % {'exception': e})

        for sample in samples:
            msg = sample.as_dict()
            LOG.debug(_('Publishing sample %(msg)s to '
                        '%(host)s:%(port)d') % {'msg': msg,
                                                'host': self.host,
                                                'port': self.port})
            try:
                host = 'openstack'
                ttl = cfg.CONF.publisher_riemann.default_ttl

                if sample.resource_metadata:
                    host = sample.resource_metadata.get('host', host)
                    ttl = sample.resource_metadata.get('ttl', ttl)

                state = 'ok'  # TODO: sample data that can be used for this?
                description = ''  # TODO
                tags = []  # TODO
                attributes = {k: v for k, v in sample.resource_metadata
                              if k not in ignore_metadata_keys}

                event = {'time': time.time(),
                         'ttl': ttl,
                         'host': host,
                         'service': sample.name,
                         'state': state,
                         'metric': sample.volume,
                         'description': description,
                         'tags': tags,
                         'attributes': attributes
                         }

                self.client.send(event)
            except Exception as e:
                LOG.warn(_('Unable to send sample'))
                LOG.exception(e)
