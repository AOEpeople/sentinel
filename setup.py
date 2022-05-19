import setuptools

setuptools.setup(name='sentinel',
                 version='0.0-build',
                 description='sentinel zero trust cli proxy',
                 author='Kevin Schu',
                 install_requires=[
                     'oic>=1.3',
                     'mitmproxy<8.1,>=8',
                     'cryptography<37,>=36'
                 ],
                 author_email='kevin.schu@aoe.com',
                 packages=setuptools.find_packages(),
                 zip_safe=False)
