## **Actividad 1**

- El proyecto original se basa en una aplicación web desarrollada para la asignatura **Proyecto Integrador 1**, cuyo código base se encuentra en el siguiente enlace: [Enlace al repositorio original](https://github.com/MateoRamirezRubio1/Senior_Companion_Service).
- En este nuevo repositorio se realizarán **refactorizaciones y mejoras** del código con el objetivo de optimizar y mejorar la calidad del proyecto. Las modificaciones se alojarán aquí para no alterar la versión original del código.
- Las mejoras incluirán la **reorganización del código**, la aplicación de **patrones de diseño** como servicios y repositorios, y mejoras relacionadas con el **rendimiento** y **mantenibilidad** del proyecto.

## **Actividad 2: Revisión Autocrítica**

En el proyecto, la aplicación está estructurada de forma monolítica, con toda la lógica del negocio y la manipulación de datos centralizada en los archivos views.py. Tras revisar los parámetros de calidad vistos en clase (Usabilidad, Compatibilidad, Rendimiento, Seguridad), identificamos algunos puntos clave que afectaban la calidad del proyecto y que debían ser mejorados. A continuación, describiremos tanto los aspectos positivos como los que podrían mejorarse, además de proponer la aplicación de inversión de dependencias para optimizar ciertas áreas.

#### 1. **Usabilidad:**
- **Aspectos que cumplen:**
    - La estructura general de la aplicación es fácil de usar para los usuarios finales, con formularios y vistas generadas en Django que se adaptan de manera sencilla a Bootstrap y HTML. La navegación en el frontend es básica pero clara.
- **Aspectos a mejorar:**
    - El código del frontend (HTML, Bootstrap, CSS, y JavaScript) es poco mantenible y desorganizado. Hay código JavaScript obsoleto o desactualizado que afecta la interactividad y dinamismo de la aplicación.
    - El uso de Bootstrap con una personalización limitada no aprovecha del todo las capacidades de un diseño responsive y accesible.
    - **Solución propuesta:** Se puede mejorar la usabilidad del frontend optimizando y reestructurando el código HTML, CSS y JavaScript. Recomendamos usar técnicas como minificación de archivos y la modularización del CSS y JS para mejorar la mantenibilidad y la velocidad de carga.

#### 2. **Compatibilidad:**
- **Aspectos que cumplen:**
    - Django es altamente compatible con diferentes plataformas, lo que garantiza que los usuarios puedan acceder a la aplicación desde una variedad de dispositivos.
- **Aspectos a mejorar:**
    - El frontend es solo HTML con Bootstrap, lo que podría afectar la compatibilidad con dispositivos móviles más antiguos o de bajo rendimiento.
    - Se puede mejorar la compatibilidad con diferentes resoluciones y pantallas optimizando el CSS y aprovechando las capacidades responsive de Bootstrap con media queries más avanzadas.
    - **Solución propuesta:** Mejorar la compatibilidad con navegadores más antiguos y optimizar el CSS para garantizar que el sitio se vea bien en una variedad más amplia de dispositivos. Modularizar el frontend para hacer más fácil la adaptación y prueba en diferentes entornos.

#### 3. **Rendimiento:**
- **Aspectos que cumplen:**
    - Django ofrece un rendimiento aceptable para aplicaciones pequeñas y medianas, y el ORM permite optimizar las consultas a la base de datos de forma eficiente.
- **Aspectos a mejorar:**
    - Templates y código HTML no están optimizados para el rendimiento. Por ejemplo, no se están utilizando técnicas como el caching de vistas en Django, lo que podría mejorar la velocidad de respuesta.
    - Actualmente no se está aplicando ningún sistema de caché para almacenar respuestas comunes o datos que se consultan repetidamente, lo que genera sobrecarga en la base de datos y en el servidor.
    - **Solución propuesta:** Implementar caching tanto en el frontend (caché de navegador) como en el backend (usando el sistema de caché de Django) para vistas que no cambian con frecuencia.
    También se podrían optimizar las consultas en las vistas de Django, y emplear servicios y repositorios (como veremos más adelante) para manejar de manera más eficiente las interacciones con la base de datos.
#### 4. **Seguridad:**
- **Aspectos que cumplen:**
    - Django incluye protección contra ataques de CSRF, gestión de contraseñas seguras, y protección contra inyecciones SQL, todo esto por defecto.
- **Aspectos a mejorar:**
    - Validaciones y permisos: Actualmente, las validaciones y permisos están implementados de manera básica en las vistas. No hay una clara separación de responsabilidades para manejar lógicas complejas de permisos o validación de datos en diferentes capas del sistema.
    - Gestión de sesiones y autenticación en el frontend no están adecuadamente optimizadas. Por ejemplo, el control de permisos y accesos en las vistas podría ser más robusto.
    - **Solución propuesta:** Refactorizar el sistema de validaciones y permisos para tener un control más estricto y detallado a nivel de servicio, asegurando que las reglas de seguridad estén centralizadas y fáciles de mantener.

### **Aplicación de la Inversión de Dependencias:**

Uno de los puntos más críticos donde se puede aplicar la Inversión de Dependencias es en la refactorización de la lógica del negocio y el acceso a datos.
Enfocandonos en la app Customer. Inicialmente, toda la lógica del negocio estaba centralizada en `views.py`, lo que generaba un fuerte acoplamiento entre la lógica de presentación (vistas) y la lógica del negocio.

#### **Problemas identificados:**

- **Acoplamiento excesivo:** El código en `views.py` mezcla lógica del negocio con el manejo de datos, lo que dificulta el mantenimiento, la prueba y la evolución del proyecto.
- **Dificultad para realizar pruebas unitarias:** Al estar la lógica del negocio tan acoplada a las vistas, resulta complicado probar las funcionalidades de manera independiente.

#### **Solución propuesta:**
- **Separación en servicios y repositorios:** Aplicamos la Inversión de Dependencias separando la lógica del negocio en servicios (que contienen las reglas de negocio) y repositorios (que manejan la interacción con la base de datos). Por ejemplo, para la app Customer, se crearon:
    - Un `services.py`, que encapsula toda la lógica relacionada con los clientes.
    - Un `repositories.py`, que maneja el acceso a la base de datos.
- Los controladores en las vistas ya no interactúan directamente con el ORM, sino que dependen de los servicios, los cuales, a su vez, dependen de los repositorios.

#### **Ventajas de la Inversión de Dependencias:**
- **Desacoplamiento:** La lógica del negocio no está directamente atada al ORM de Django, lo que facilita cambiar la implementación de acceso a datos en el futuro (por ejemplo, cambiar de una base de datos SQL a NoSQL).
- **Testeo más sencillo:** Al desacoplar la lógica de negocio del acceso a datos y de las vistas, es mucho más sencillo crear pruebas unitarias para cada componente.
- **Mantenibilidad y extensibilidad:** Esta estructura hace que sea más fácil agregar nuevas funcionalidades o modificar las existentes sin afectar otras partes del sistema.

#### **Conclusión:**
La revisión autocrítica ha revelado varias áreas que pueden mejorarse en términos de calidad, especialmente en rendimiento, mantenibilidad, y seguridad. Aplicar técnicas como caching, mejorar la estructura del frontend, y refactorizar la lógica del negocio mediante la Inversión de Dependencias ayuda a que la aplicación sea más fácil de mantener y optimizar. Esto también prepara la base para escalar la aplicación en el futuro, ya que una arquitectura modular y bien separada facilita la incorporación de nuevas funcionalidades y servicios sin comprometer la calidad del software.

## **Actividad 3: Inversión de Dependencias**

La Inversión de Dependencias es un principio fundamental del diseño orientado a objetos que promueve que las clases de alto nivel no dependan de clases de bajo nivel, sino de abstracciones. Esto significa que tanto los módulos de alto como de bajo nivel deberían depender de interfaces o abstracciones comunes, no de implementaciones concretas.

En nuestro proyecto, este principio se aplicó creando interfaces abstractas para los repositorios, de manera que los servicios dependen de estas abstracciones y no de la implementación específica de un repositorio.

### **Ejemplos Concretos:**
#### 1. **Interfaz abstracta para repositorios:**
Aquí se define una clase abstracta que contiene métodos genéricos, como `get_by_user_id`, que luego serán implementados por las clases concretas de los repositorios.

```python
from abc import ABC, abstractmethod

class AbstractCustomerRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id):
        pass
```

- **Propósito:** Desacoplar la lógica de negocio de la implementación específica del repositorio, permitiendo el cambio de repositorios sin afectar el servicio.

#### 2. **Servicio que depende de la abstracción y no de la implementación concreta:**
El servicio de `CustomerService` recibe en su constructor una implementación del repositorio, pero esta implementación debe cumplir con la interfaz abstracta (`AbstractCustomerRepository`), lo que asegura que el servicio puede trabajar con cualquier repositorio que implemente esa interfaz, sin importar su implementación.

```python
class CustomerService:
    def __init__(self, customer_repository: AbstractCustomerRepository):
        self.customer_repository = customer_repository

    def get_customer_by_user_id(self, user_id):
        return self.customer_repository.get_by_user_id(user_id)
```

- **Beneficio:** El servicio no sabe ni le importa cómo funciona el repositorio internamente; solo sabe que puede llamar a los métodos que la interfaz garantiza.

#### 3. **Repositorio concreto que implementa la abstracción:**
Finalmente, una clase concreta como `CustomerRepository` implementa la interfaz `AbstractCustomerRepository`, proporcionando la funcionalidad específica de acceso a la base de datos.

```python
class CustomerRepository(AbstractCustomerRepository):
    def get_by_user_id(self, user_id):
        return self.model.objects.get(idUser=user_id)
```

- **Ventaja:** Este repositorio concreto puede ser fácilmente reemplazado o modificado sin cambiar la lógica del servicio, ya que el servicio solo conoce la interfaz.

### **Beneficios:**
- **Desacoplamiento:** Las clases de alto nivel (servicios) no dependen de implementaciones específicas, sino de abstracciones, lo que permite cambiar las implementaciones sin afectar la lógica de negocio.
- **Facilidad de Testeo:** Los servicios pueden ser probados fácilmente utilizando mocks o stubs, ya que dependen de interfaces, no de implementaciones concretas.
- **Escalabilidad y Flexibilidad:** Es sencillo agregar nuevas implementaciones de repositorios (por ejemplo, cambiar una base de datos relacional por una no relacional) sin tener que modificar los servicios.


## **Actividad 4: Aplicación de Patrones de Diseño (Factory y Decorator)**

En esta actividad, aplicamos dos patrones de diseño muy útiles: Factory y Decorator. Estos patrones nos ayudan a organizar mejor el código, haciéndolo más flexible, modular, y fácil de mantener.

### 1. **Patrón Factory:**
El patrón Factory se usa cuando se necesita crear objetos de manera controlada y flexible. En nuestro caso, hemos implementado una fábrica que se encarga de crear instancias de servicios y sus repositorios asociados. Esto permite que la lógica de creación de estos objetos esté centralizada en un solo lugar, y que las clases que los usan no tengan que preocuparse por cómo se crean.

#### **Ejemplo del Patrón Factory:**

```python
class ServiceFactory:
    """
    Factory to create instances of services with their associated repositories.
    """

    def get_service(self, service_type: str):
        """
        Returns the appropriate service based on the specified type.

        """

        services = {
            "CUSTOMER": lambda: CustomerService(CustomerRepository()),
            "PREFERENCE": lambda: PreferenceService(PreferenceRepository()),
            "MEDICAL_INFO": lambda: MedicalInformationService(
                MedicalInformationRepository()
            ),
        }

        if service_type not in services:
            raise ValueError(f"The service type '{service_type}' is not supported.")

        return services[service_type]()
```

#### **Mejora que proporciona el patrón Factory:**

- **Centralización de la Lógica de Creación:** La creación de objetos relacionados (servicios y sus repositorios) está en un solo lugar. Esto hace que el código sea más fácil de modificar si alguna vez cambiamos la manera en que se crean los servicios.
- **Reducción de la Complejidad en las Clases que Usan Servicios:** Las clases o vistas que necesitan servicios no tienen que preocuparse por cómo se crean los mismos; solo llaman a la fábrica.

### 2. **Patrón Decorator:**
El patrón Decorator permite extender o modificar el comportamiento de una función o clase sin modificar su estructura original. En este proyecto, hemos utilizado un decorador para agregar funcionalidad a las vistas, específicamente, para verificar y obtener el cliente actual asociado al usuario autenticado antes de ejecutar la vista.

#### **Ejemplo del Patrón Decorator:**

```python
def actual_customer_required(customer_service):
    """
    Decorator to obtain the current customer associated with the logged-in user.
    Adds the current customer as an argument to the view.

    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            actual_user_id = request.user.idUser

            # Use the service to obtain the current customer
            actual_customer = customer_service.get_customer_by_user_id(actual_user_id)

            if actual_customer is None:
                return HttpResponseForbidden(
                    "No customer associated with the user was found."
                )

            # Add the current customer to the view context
            return view_func(request, actualCustomer=actual_customer, *args, **kwargs)

        return _wrapped_view

    return decorator
```

#### **Mejora que proporciona el patrón Decorator:**

- **Reutilización de Código:** En lugar de escribir la misma lógica de verificación en cada vista, el decorador nos permite aplicar esta verificación de forma reutilizable y consistente en cualquier vista que lo necesite.
- **Modularidad y Separación de Responsabilidades:** La lógica para obtener el cliente actual se separa de la lógica principal de la vista, lo que mejora la legibilidad del código y la organización.
- **Extensibilidad:** Si en el futuro queremos agregar más lógica (por ejemplo, verificar permisos adicionales), podemos hacerlo en el decorador sin modificar las vistas originales.

## **Conclusión**
Los patrones Inversión de Dependencias, Factory, y Decorator han mejorado significativamente la calidad del código en nuestro proyecto.

- La Inversión de Dependencias nos permite desacoplar la lógica de negocio de los detalles de implementación de los repositorios, haciéndolo más flexible, escalable, y fácil de probar.
- El Factory simplifica la creación de objetos y promueve la centralización de la lógica de creación, lo que facilita la modificación y el mantenimiento del código.
- El Decorator nos permite agregar comportamiento adicional a las funciones de forma modular y reutilizable, mejorando la organización del código y la separación de responsabilidades.

Estas mejoras hacen que el proyecto sea más fácil de mantener y extender en el futuro, promoviendo un diseño limpio y orientado a patrones sólidos.