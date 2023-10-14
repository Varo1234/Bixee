$(document).ready(function() {
	$('#taskModal2').on('show.bs.modal', function (event) {
	    var button = $(event.relatedTarget);  // Botón que disparó el modal
	    var name = button.data('name');       // Extrae el nombre de la tarea
	    var description = button.data('description'); // Extrae la descripción de la tarea
	    var id = button.data('id');           // Extrae el id de la tarea
	    var project_id = button.data('project_id'); // Extrae el id del proyecto
	    // Actualiza los campos del modal
	    var modal = $(this);
	    modal.find('input[placeholder="Edit Title"]').val(name);
	    modal.find('textarea[placeholder="Add description"]').val(description);
	    modal.find('input[name="task_id"]').val(id);
		//pasar el id de la tarea al form
		modal.find('form').attr('action', '/projects/' + project_id + '/task/' + id + '/edit/', view='edit_task');
	});

	// actualizar el estado de la tarea
	 $('.checkbox').on('change', function() {
        var taskId = $(this).data('task-id');  // Asegúrate de agregar un atributo data-task-id en tu input
        var project_id = $(this).data('project-id');
        var isChecked = $(this).prop('checked');

        $.post({
            url: '/projects/' + project_id + '/task/' + taskId + '/toggle/',  // URL a la que se enviará la solicitud
            data: {
                'task_id': taskId,
                'project_id': project_id,
                'completed': isChecked,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()  // Token CSRF para seguridad
            },
            success: function(response) {
                // Aquí puedes manejar la respuesta, por ejemplo, mostrar un mensaje de éxito.
            },
            error: function(error) {
                // Aquí puedes manejar cualquier error que ocurra, por ejemplo, revertir el checkbox a su estado anterior.
            }
        });
    });
	// actualizar importancia de la tarea
	 $('.task-important').on('click', function(e) {
        e.preventDefault();

        var taskId = $(this).data('task-id-important');
        var project_id = $(this).data('project-id');
        $.post({
         url: '/projects/' + project_id + '/task/' + taskId + '/toggle_important/',  // URL a la que se enviará la solicitud
         data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()  // Token CSRF para seguridad
            },
            success: function(response) {
            	if (response.important) {
					 $('a[data-task-id-important=' + taskId + ']').addClass('active');
				} else {
					 $('a[data-task-id-important=' + taskId + ']').removeClass('active');
				}
			},
			error: function(error) {
				console.log(error);
            }
        });
    });

    $('#btn-check-2-outlined').on('click', function(e) {
		console.log('click');
		var projectId = $(this).data('project-id');
		$.post({
		 url: '/projects/' + projectId + '/complete/',  // URL a la que se enviará la solicitud
		 data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()  // Token CSRF para seguridad
			},
			success: function(response) {
				if (response.completed) {
					 $('a[data-project-id=' + projectId + ']').addClass('btn-success');
				} else {
					 $('a[data-project-id=' + projectId + ']').removeClass('btn-success');
				}
		    },
		    error: function(error) {
				console.log(error);
			}
		});
	});
	$(document).ready(function () {
        $('#asignado_a a').click(function () {
            $('#selectedUserInput').val($(this).text());
        });
    });
});
