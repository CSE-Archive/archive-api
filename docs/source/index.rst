CSE Archive API Endpoints
=========================

| Currently with this implementation, database is read-only and just GET methods are needed and available, other operations like POST a new resource are limited to admins in admin site.
| If you are a front-end developer and want to build a web, mobile, telegram bot or other applications based on this API, or just want to use it personally, here you can find all endpoints paramethers and their call results in details.


.. raw:: html

    <style> .red {color:#aa0060; font-weight:bold; font-style: italic} </style>

.. role:: red


.. toctree::
   :hidden:

   courses/index
   references/index
   resources/index
   classrooms/index
   teachers/index


Courses
~~~~~~~

.. list-table::
   :widths: 20 50 50
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `get <courses/get.html>`_
     - GET */courses/*:red:`courseId`
     - Gets a course by ID.
   * - `list <courses/list.html>`_
     - GET */courses*
     - Lists courses.


References
~~~~~~~~~~

.. list-table::
   :widths: 20 50 50
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `get <references/get.html>`_
     - GET */references/*:red:`referenceId`
     - Gets a reference by ID.
   * - `list <references/list.html>`_
     - GET */references*
     - Lists references.


Resources
~~~~~~~~~

.. list-table::
   :widths: 20 50 50
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `get <resources/get.html>`_
     - GET */resources/*:red:`resourceId`
     - Gets a resource by ID.
   * - `list <resources/list.html>`_
     - GET */resources*
     - Lists resources.


Classrooms
~~~~~~~~~~

.. list-table::
   :widths: 20 50 50
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `get <classrooms/get.html>`_
     - GET */classrooms/*:red:`classroomId`
     - Gets a classroom by ID.
   * - `list <classrooms/list.html>`_
     - GET */classrooms*
     - Lists classrooms.


Teachers
~~~~~~~~

.. list-table::
   :widths: 20 50 50
   :header-rows: 1

   * - Method
     - HTTP request
     - Description
   * - `get <teachers/get.html>`_
     - GET */teachers/*:red:`teacherId`
     - Gets a teacher by ID.
   * - `list <teachers/list.html>`_
     - GET */teachers*
     - Lists teachers.
