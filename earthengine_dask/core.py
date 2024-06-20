# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_core.ipynb.

# %% auto 0
__all__ = ['InitEarthEngine', 'ClusterGEE', 'LocalClusterGEE']

# %% ../00_core.ipynb 3
import coiled
import dask.distributed
import ee
import google.auth

# %% ../00_core.ipynb 4
class InitEarthEngine(dask.distributed.WorkerPlugin):
    def __init__(self, **kwargs):
        print('InitEarthEngine.init: starting')  # This appears in the notebook output where the cluster is initiated.
        self.kwargs = kwargs
        print(f'InitEarthEngine.init: kwargs = {kwargs}')

    def setup(self, worker):
        # Print statements output to the dask cluster logs (viewable via Coiled dashboard)
        print('InitEarthEngine.setup: starting')
        print('InitEarthEngine.setup: default to using the high volume endpoint')
        self.kwargs.setdefault('opt_url', 'https://earthengine-highvolume.googleapis.com')
        import ee
        print(f'InitEarthEngine.setup: ee.Initialize(**{self.kwargs})')
        ee.Initialize(**self.kwargs)


class ClusterGEE(coiled.Cluster):
    def __init__(self, **kwargs):
        print('ClusterGEE init')
        super().__init__(**kwargs)
        # Wait for the workers to start, then send the ADCs
        self.wait_for_workers(kwargs['n_workers'])
        coiled.credentials.google.send_application_default_credentials(self)

    def get_client(self):
        print('ClusterGEE get_client')
        client = super().get_client()
        client.register_plugin(InitEarthEngine())
        return client


# For local development
class LocalClusterGEE(dask.distributed.LocalCluster):    
    def __init__(self, **kwargs):
        print('LocalClusterGEE init')
        super().__init__(**kwargs)

    def get_client(self):
        print('LocalClusterGEE get_client')
        client = super().get_client()
        client.register_plugin(InitEarthEngine())
        return client
