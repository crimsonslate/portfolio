Glossary
========

======
Models
======

.. py:class:: MediaCategory

    A user created collection of :py:class:`Media`.

    .. py:attribute:: name

        **Required.** A short name.

        Maximum 64 characters.

        :type: :py:class:`str`

    .. py:attribute:: cover

        *Optional.* A cover image.

        :type: :py:class:`~django.core.files.File` | :py:type:`None`
        :value: ``None``

.. py:class:: Media

    A user created published work.

    .. py:attribute:: title

        **Required**. A short title.

        Maximum 64 characters. Must be unique.

        :type: :py:class:`str`

    .. py:attribute:: source

        **Required**. A video or an image.

        :type: :py:class:`~django.core.files.File`

    .. py:attribute:: thumb

        *Optional*. A thumbnail image.

        Automatically generated on save if the media is a video.

        :type: :py:class:`~django.core.files.File` | :py:type:`None`
        :value: ``None``

    .. py:attribute:: subtitle

        *Optional*. A medium-length subtitle.

        Maximum 128 characters.

        :type: :py:class:`str` | :py:type:`None`
        :value: ``None``

    .. py:attribute:: desc

        *Optional*. A lengthy description.

        Maximum 2048 characters.

        :type: :py:class:`str` | :py:type:`None`
        :value: ``None``

    .. py:method:: generate_thumbnail([loc=0]) -> File

        Generates a thumbnail at frame ``loc``.

        :param loc: The frame of the media to generate. Default is 0.
        :type loc: :py:class:`int`
        :return: A new thumbnail file.
        :rtype: :py:class:`~django.core.files.File`
        :raises ValueError: If the media is an image.
