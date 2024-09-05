(defrule ingreso-vehiculo
   (vehiculo (matricula ?matricula) (tipo ?tipo))
   (espacio (id ?id) (tipo ?tipo) (ocupado FALSE))
   =>
   (assert (vehiculo-ubicado (matricula ?matricula) (id ?id)))
   (retract (espacio (id ?id) (tipo ?tipo) (ocupado FALSE)))
   (assert (espacio (id ?id) (tipo ?tipo) (ocupado TRUE)))
)

(defrule salida-vehiculo
   (vehiculo-ubicado (matricula ?matricula) (id ?id))
   =>
   (retract (vehiculo-ubicado (matricula ?matricula) (id ?id)))
   (assert (espacio (id ?id) (tipo GENERAL) (ocupado FALSE)))
)