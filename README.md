# ENUNCIADO

La empresa '' nos contrata para obtener conocimiento de los restaurantes y de los hábitos de consumo de los comensales. Para ello, nos plantea el siguiente escenario: Quiere dirigirse a los restaurantes ofreciéndoles un servicio de publicidad y recomendación de los menús diarios. El funcionamiento, a alta nivel, sería el siguiente:

- Los restaurantes envían diariamente un pdf con el menú diario que ofrece. En el caso de no tener menú diario o querer promocionar la carta, enviarán un pdf con los platos que tienen en carta.

- El usuario final, comensal, se conectará a una página web en la que podrá hacer diferentes consultas para que el sistema le recomiende los restaurantes que ese día le ofrecen la oferta que está buscando. Podrá buscar por alguna o por cualquier combinación de:
  - Por platos, tanto en el menú diario como en la carta
  - Por ubicación
  - Por tipología de restaurante
  - Por tipo de menú (sin restricciones, celiaco, vegetariano, vegano, ...)
  - Por precio

- El usuario (comensal) podrá reservar en la web el restaurante, con los platos que quiere. Si no hace esta reserva, en el restaurante, al tomarle la comanda, rellenarán también los platos que ha solicitado el comensal.

- Posteriormente, el comensal podrá valorar tanto los platos que ha consumido, como el restaurante.

Por otro lado, el restaurante puede estar interesado en promocionar algún plato. Durante el periodo de esta promoción, el restaurante tendrá que pagar un importe diario para conseguir que su posición en el resultado de la búsqueda se vea mejorada.

- De los resultados que se muestran al comensal, en la búsqueda en la web, el orden se puede ver modificado por:
  - Valoración del cliente del restaurante
  - Valoración del cliente de los platos
  - Pago de promoción del plato
- Para ello:
  - Quiere tener una base de datos en la que gestionar
  - Los restaurantes que estén subscritos al programa, con todos los datos necesarios
  - Las valoraciones de los platos por parte de los comensales 
  - Las valoraciones de los restaurantes por parte de los comensales
  - Las promociones activas asociadas a los platos
  - Necesita un almacenamiento en el que guardar los pdfs o imágenes con los menús diarios y/o cartas menús.
  - Montar un almacén de conocimiento en el que se pueda buscar la información, como se ha descrito en los puntos anteriores.

## Objetivo de la práctica: Crear la base de conocimiento para explotar esta información y hacer búsquedas sobre ella.

Adicionalmente, implementar la aplicación que de soporte al sistema.

### Fecha entrega: 27 
