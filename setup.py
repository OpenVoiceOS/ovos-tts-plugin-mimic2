#!/usr/bin/env python3
from setuptools import setup

PLUGIN_ENTRY_POINT = 'catotron_tts_plug = ' \
                     'mycroft_tts_plugin_catotron:CatotronTTSPlugin'
setup(
    name='mycroft-tts-plugin-catotron',
    version='0.1.1',
    description='A catalan tacotron based tts plugin for mycroft',
    url='https://github.com/JarbasIberianLanguageResources/mycroft-tts-plugin-catotron',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['mycroft_tts_plugin_catotron'],
    install_requires=["requests", "pydub"],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft plugin tts',
    entry_points={'mycroft.plugin.tts': PLUGIN_ENTRY_POINT}
)
