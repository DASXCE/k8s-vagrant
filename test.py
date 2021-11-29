# -*- coding: utf-8 -*-
"""
Set First Data specific grains decoded from server name.

The following grains will be defined:
  - fd_region
  - fd_country
  - fd_country_iso
  - fd_state
  - fd_location
  - fd_office
  - fd_type
  - fd_os
  - fd_environment
  - fd_role
  - fd_instance
"""
import sys
import json

# Import python libs
import platform
import logging

# Set up logging
log = logging.getLogger(__name__)

# get lowercase hostname
#hostname = platform.node().split(".")[0].lower()
hostname = sys.argv[1]

# get information from hostname as defined per FD naming schema
try:
    os = hostname[0]
    location = hostname[1]
    environment = hostname[2]
    type = hostname[3]
    role = hostname[4:6]
    instance = hostname[6:]
except:
    # hostname doesn't conform to our standard
    # include a class which notifies us of the problem
    raise SystemExit('Hostname %s doesn\'t conform to First Data standard' % hostname)

# map oses from hostname into os
oses = {}
oses['a'] = 'aix'
oses['d'] = 'centos'
oses['l'] = 'linux'
oses['n'] = 'suse'
oses['o'] = 'oracle'
oses['r'] = 'redhat'
oses['w'] = 'windows'
try:
    os = oses[os]
except:
    os = 'undef'

# map locations from filename to data center type
dc_types = {}
dc_types['1'] = 'dc'
dc_types['3'] = 'dr'
dc_types['4'] = 'dc'
dc_types['5'] = 'dr'
dc_types['b'] = 'dc'
dc_types['a'] = 'dr'
dc_types['i'] = 'dc'
dc_types['j'] = 'dr'
dc_types['k'] = 'dc'
dc_types['l'] = 'dr'

dc_types['x'] = 'dc'
try:
    dc_type = dc_types[location]
except:
    dc_type = 'undef'

# map locations from hostname into locations
locations = {}
locations['1'] = 'omaha'
locations['3'] = 'chandler'
locations['4'] = 'eshelter'
locations['5'] = 'equinix'
locations['a'] = 'tutoia'
locations['b'] = 'hortolandia'
locations['i'] = 'mumbai'
locations['j'] = 'chennai'
locations['k'] = 'parque_patricios'
locations['l'] = 'peru'

locations['x'] = 'bijela'
try:
    location = locations[location]
except:
    location = 'undef'

remote_locations = {}
remote_locations['omaha'] = 'chandler'
remote_locations['chandler'] = 'omaha'
remote_locations['eshelter'] = 'equinix'
remote_locations['equinix'] = 'eshelter'
remote_locations['tutoia'] = 'hortolandia'
remote_locations['hortolandia'] = 'tutoia'
remote_locations['mumbai'] = 'chennai'
remote_locations['chennai'] = 'mumbai'
remote_locations['parque_patricios'] = 'peru'
remote_locations['peru'] = 'parque_patricios'

# no remote for bijela
remote_locations['bijela'] = 'undef'

try:
    remote_location = remote_locations[location]
except:
    office = 'undef'

# map offices from locations into office
offices = {}
offices['omaha'] = 'Atlanta'
offices['chandler'] = 'Atlanta'
offices['eshelter'] = 'Bad Vilbel'
offices['equinix'] = 'Bad Vilbel'
offices['tutoia'] = 'Sao Paulo'
offices['hortolandia'] = 'Sao Paulo'
offices['parque_patricios'] = 'Buenos Aires'
offices['peru'] = 'Buenos Aires'

offices['bijela'] = 'Bijela'
try:
    office = offices[location]
except:
    office = 'undef'

# map states from locations into states
states = {}
states['omaha'] = 'Georgia'
states['chandler'] = 'Georgia'
states['eshelter'] = 'Hessen'
states['equinix'] = 'Hessen'
states['tutoia'] = 'Sao Paulo'
states['hortolandia'] = 'Maranhao'
states['mumbai'] = 'Maharashtra'
states['chennai'] = 'Tamil Nadu'
states['parque_patricios'] = 'Buenos Aires'
states['peru'] = 'Buenos Aires'

states['bijela'] = 'Herceg-Novi'
try:
    state = states[location]
except:
    state = 'undef'

# map regions from locations in hostname into countries
countries = {}
countries['omaha'] = 'usa'
countries['chandler'] = 'usa'
countries['eshelter'] = 'germany'
countries['equinix'] = 'germany'
countries['tutoia'] = 'brazil'
countries['hortolandia'] = 'brazil'
countries['mumbai'] = 'india'
countries['chennai'] = 'india'
countries['parque_patricios'] = 'argentina'
countries['peru'] = 'argentina'

countries['bijela'] = 'montenegro'
try:
    country = countries[location]
except:
    country = 'undef'

# map iso country code from countries countries_iso
countries_iso = {}
countries_iso['usa'] = 'US'
countries_iso['germany'] = 'DE'
countries_iso['brazil'] = 'BR'
countries_iso['india'] = 'IN'
countries_iso['argentina'] = 'AR'

countries_iso['montenegro'] = 'ME'
try:
    country_iso = countries_iso[country]
except:
    country_iso = 'undef'

# map regions from countries
regions = {}
regions['usa'] = 'na'
regions['germany'] = 'emea'
regions['india'] = 'apac'
regions['brazil'] = 'lac'
regions['argentina'] = 'latam'

regions['montenegro'] = 'mne'
try:
    region = regions[country]
except:
    region = 'undef'

# map environment from hostname into environment
environments = {}
environments['p'] = 'prod'
environments['c'] = 'cat'
environments['q'] = 'qa'
environments['d'] = 'dev'
environments['t'] = 'test'
environments['b'] = 'backup'
try:
    environment = environments[environment]
except:
    environment = 'undef'

# map type from hostname into type
types = {}
types['p'] = 'physical'
types['v'] = 'virtual'
try:
    type = types[type]
except:
    type = 'undef'

# map role from hostname into role
roles = {}
roles['ap'] = 'appserver'
roles['wb'] = 'webserver'
roles['db'] = 'dbserver'
roles['ir'] = 'irserver'
try:
    role = roles[role]
except:
    role = 'undef'


def server_info():
    """Set server classification grains decoded from host name."""
    grains = {}
    grains['fd_region'] = region
    grains['fd_country'] = country
    grains['fd_country_iso'] = country_iso
    grains['fd_state'] = state
    grains['fd_location'] = location
    grains['fd_remote_location'] = remote_location
    grains['fd_dc_type'] = dc_type
    grains['fd_office'] = office
    grains['fd_type'] = type
    grains['fd_os'] = os
    grains['fd_environment'] = environment
    grains['fd_role'] = role
    grains['fd_instance'] = instance

    print json.dumps(grains, indent=1)
    return grains

server_info()
