========================
Carson Living Python API
========================

.. image:: https://badge.fury.io/py/carson-living-electric-boogaloo.svg
    :target: https://badge.fury.io/py/carson-living-electric-boogaloo

.. image:: https://github.com/lowlydba/python-carson-living/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/lowlydba/python-carson-living/actions/workflows/ci.yml

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0

.. image:: https://img.shields.io/pypi/pyversions/carson-living-electric-boogaloo.svg
    :target: https://pypi.org/project/carson-living-electric-boogaloo/

Python Carson Living is a library written in Python that exposes the carson.live devices as Python objects.

.. warning::

    Use this library at your own risk. It may violate the `Terms of Service of Carson <https://www.carson.live/terms>`_.

Tutorial
--------
This walks through installing the library, logging in, and opening a unit door end to end.

Install the package
~~~~~~~~~~~~~~~~~~~~
Carson Living Python requires **Python 3.11 or newer**.

.. code-block::

    pip install carson-living-electric-boogaloo

Log in and inspect the account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    from carson_living import Carson

    carson = Carson("account@email.com", "your password")
    print(carson.user)
    # >> Martin
    print(carson.token)
    # >> ey...

Carson Living issues long-lived JWT tokens. Copy the printed ``carson.token`` value now;
`Reuse a saved token`_ below covers skipping the login request on future runs.

Open a unit door
~~~~~~~~~~~~~~~~
.. code-block:: python

    for door in carson.first_building.doors:
        if door.is_unit_door:
            print("Opening Unit Door {}".format(door.name))
            door.open()

How-to guides
-------------

Reuse a saved token
~~~~~~~~~~~~~~~~~~~
Pass a saved JWT token during initialization to skip the login request:

.. code-block:: python

    carson = Carson("account@email.com", "your password", "ey....")
    print(carson.token)
    # >> ey...

Save a live camera image
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    for camera in building.cameras:
        with open("image_{}.jpeg".format(camera.entity_id), "wb") as file:
            camera.get_image(file)

Save a live camera video
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    for camera in building.cameras:
        with open("video_{}.flv".format(camera.entity_id), "wb") as file:
            camera.get_video(file, timedelta(seconds=10))

Download a recorded image from a timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    three_hours_ago = datetime.utcnow() - timedelta(hours=3)
    for camera in building.cameras:
        with open("image_{}.jpeg".format(camera.entity_id), "wb") as file:
            camera.get_image(file, three_hours_ago)

Download a recorded video from a timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    three_days_ago = datetime.utcnow() - timedelta(days=3)
    for cam in building.cameras:
        with open("video_{}.flv".format(cam.entity_id), "wb") as file:
            cam.get_video(file, timedelta(seconds=5), three_days_ago)

Generate an authenticated camera URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``camera.get_image_url()`` and ``camera.get_video_url()`` build a URL with an embedded
``auth_key`` (``A=c000....``) that something outside this library can fetch directly.
Call ``building.eagleeye_api.update_session_auth_key()`` first if the building's key may
be stale; ``get_image()`` and ``get_video()`` don't need this since they refresh internally.

.. code-block:: python

    building.eagleeye_api.update_session_auth_key()
    for cam in building.cameras:
        img_url = cam.get_image_url(three_days_ago)
        print(img_url)
        # >> https://cXXX.eagleeyenetworks.com/asset/prev/image.jpeg?id=c0&timestamp=20200122211442.575&asset_class=pre&A=c000~...
        response = requests.get(img_url)
        with open("image_{}_with_url.jpeg".format(cam.entity_id), "wb") as file:
            file.write(response.content)
        break  # only fetch one camera in this example

Use ``cam.get_video_url()`` the same way.

Use the CLI tool
~~~~~~~~~~~~~~~~~
``./scripts/carsoncli.py`` has further API usage examples.

Reference
---------

Supported entities
~~~~~~~~~~~~~~~~~~~
- User (``carson.user``): read
- Building (``carson.buildings``): read
- Doors (``building.doors``): read, open
- Cameras (``building.cameras``): read, images, video

Not yet supported
~~~~~~~~~~~~~~~~~~
- Visitor functionality (``/visitors``)
- Thread / messaging functionality (``/threads``)
- Delivery functionality (``/deliveries``)
- Dashboard functionality (``/dashboard``)
- Service functionality (``/service``)
- Twilio integration (``twilio/access-token/``)
- A separate EagleEye API package

Install the development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

    pip install git+https://github.com/lowlydba/python-carson-living@main

Explanation
-----------

Why tokens are long-lived
~~~~~~~~~~~~~~~~~~~~~~~~~
Carson Living issues JWT tokens with a long validity window, so this library treats
``carson.token`` as reusable across process restarts rather than something to re-fetch on
every run. It also handles expired tokens and the resulting 401 responses internally, so a
caller doesn't need to check token validity before making a request.

Why Eagle Eye auth keys need refreshing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``get_image()`` and ``get_video()`` refresh the Eagle Eye ``auth_key`` on demand, but a
pre-generated URL from ``get_image_url()``/``get_video_url()`` embeds whatever key was
current at call time and stops working once that key expires. The key is scoped to a
building rather than a single camera, so one ``update_session_auth_key()`` call covers
every camera in that building.

Code documentation style
~~~~~~~~~~~~~~~~~~~~~~~~~
Docstrings follow the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`_.

Git branching strategy
~~~~~~~~~~~~~~~~~~~~~~
This project uses `gitflow <https://nvie.com/posts/a-successful-git-branching-model/>`_ as its branching model.

Credits
~~~~~~~
This project is a fork of `pbrink231/python-carson-living <https://github.com/pbrink231/python-carson-living>`_,
itself forked from Martin Riedel's original `rado0x54/python-carson-living <https://github.com/rado0x54/python-carson-living>`_.

Project setup and the API object design were inspired by, and partly launched off,
`python-ring-doorbell <https://github.com/tchellomello/python-ring-doorbell>`_, which saved
a lot of headaches with tox, setuptools, and Travis.