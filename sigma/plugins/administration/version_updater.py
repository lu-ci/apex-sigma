import yaml
import arrow
from config import DevMode


async def version_updater(ev):
    if DevMode:
        with open('VERSION', 'r') as version_file:
            current_version_data = yaml.load(version_file)
        beta = current_version_data['beta']
        build_date = arrow.utcnow().timestamp
        major = current_version_data['version']['major']
        minor = current_version_data['version']['minor']
        patch = current_version_data['version']['patch'] + 1
        codename = current_version_data['codename']
        data_out = {
            'beta': beta,
            'build_date': build_date,
            'version': {
                'major': major,
                'minor': minor,
                'patch': patch
            },
            'codename': codename
        }
        with open('VERSION', 'w') as version_out:
            yaml.dump(data_out, version_out, default_flow_style=False)
        ev.log.info('Updated Version File.')
