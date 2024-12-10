Model Reference
===============

.. py:module:: django.core.files
.. py:module:: crimsonslate_portfolio


.. py:class:: Media

    .. py:attribute:: title

        Required. Must be unique.

        Max length of 64 characters.

        :type: :py:type:`str`
    

    .. py:attribute:: source

        Required. An image or a video.

        :type: :py:type:`File django.core.files.File`

    .. py:attribute:: thumb

        An image. Automatically generated for videos.

        :type: :py:type:`File` | :py:type:`None`
        :value: :py:type:`None`

    .. py:attribute:: subtitle

        Subtitle for this media.

        Max length of 128 characters.

        :type: :py:type:`str` | :py:type:`None`
        :value: :py:type:`None`

    .. py:attribute:: desc

        Description for this media.

        Max length of 2048 characters.

        :type: :py:type:`str` | :py:type:`None`
        :value: :py:type:`None`

    .. py:attribute:: slug

        Automatically generated slug for this media.

        :type: :py:type:`str` | :py:type:`None`
        :value: :py:type:`None`

    .. py:attribute:: is_hidden

        Manually set by user.

        If true, this media is not sent up to the front-end.

        :type: :py:type:`bool`
        :value: :py:type:`False`

    .. py:attribute:: is_image

        Automatically set.

        To be used by front-end logic, i.e. template tags.

        :type: :py:type:`bool`
        :value: :py:type:`False`

    .. py:attribute:: categories

        Categories this media is assigned to.

        :type: :py:type:`list[MediaCategory]` | :py:type:`None`
        :value: :py:type:`None`

    .. py:attribute:: date_created

        Automatically set.

        Can be updated after media creation.

        :type: :py:type:`date`

    .. py:attribute:: datetime_published

        Automatically set.

        Cannot be changed, used by the application for archiving.

        :type: :py:type:`datetime`

    .. py:method:: set_thumbnail([file=None])

        Set the media's thumbnail to the new file.

        If :py:obj:`file` is :py:type:`None`, sets the thumbnail to the result of :py:meth:`generate_thumbnail`.

        :param file: The new thumbnail.
        :type file: :py:type:`File` | :py:type:`None`
        :returns: Nothing.
        :rtype: :py:type:`None`
        :raises ValueError: If the media is an image.

    .. py:method:: generate_thumbnail([loc=0])

        Generate a thumbnail based on this media.

        The media cannot be an image.

        :param loc: Frame to capture.
        :type loc: :py:type:`int`
        :returns: The generated thumbnail.
        :rtype: :py:type:`File`
        :raises ValueError: If the media is an image.

    .. py:property:: dimensions

        If the media is a non-image, this property refers to the media's thumbnail dimensions.

        :type: :py:type:`tuple[int, int]`

    .. py:property:: file_extension

        The media's current file extension.

        :type: :py:type:`str`

    .. py:property:: url

        A URL pointing to the media's source.

        This property is an alias for :literal:`self.source.url`.

        :type: :py:type:`str`


.. py:class:: MediaCategory

    .. py:attribute:: name
    
        The name of the category.

        :type: :py:type:`str`

    .. py:attribute:: cover

        A cover image representing the category.

        :type: :py:type:`str` | :py:type:`None`
        :value: :py:type:`None` 
