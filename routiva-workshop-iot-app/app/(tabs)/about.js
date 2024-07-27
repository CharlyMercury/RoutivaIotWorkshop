import { Screen } from "../../components/Screen";
import { ScrollView, Text } from "react-native";
// import { FirebasePush } from "../../components/FirebasePush";

export default function About() {
  return (
    <Screen>
      <ScrollView>
        <Text className="text-white font-bold mb-8 mt-2 text-2xl">
          Taller de IoT: Construyendo Soluciones Conectadas con AWS Descripción
          general
        </Text>
        <Text className="text-white text-white/90 mb-4">
          Bienvenido al Taller de IoT: Construyendo Soluciones Conectadas con
          AWS. Este Workshop te guiará a través del proceso de diseñar,
          desarrollar y desplegar soluciones de Internet de las Cosas (IoT)
          utilizando una variedad de servicios de AWS. Adquirirás experiencia
          práctica en la recolección, procesamiento y visualización de datos de
          telemetría en tiempo real desde dispositivos IoT.
        </Text>
        <Text className="text-white font-bold mb-8 mt-2 text-xl">
          Agenda del Taller
        </Text>
        <Text className="text-white text-white/90 mb-4">
          Hora 1: Introducción y Configuración Introducción al IoT: Descripción
          general del IoT y sus aplicaciones. AWS IoT Core: Introducción a AWS
          IoT Core y sus componentes. Configuración de tu Entorno: Instalación
          del software necesario y configuración de los servicios de AWS.
          Ejercicio Práctico 1: Conectando un dispositivo IoT simple a AWS IoT
          Core. Ejercicio Práctico 2: Enviando datos de telemetría a AWS IoT
          Core y activando notificaciones de SNS. Recolección de Datos de
          Telemetría: Entendiendo cómo recolectar y enviar datos de telemetría
          desde dispositivos IoT. AWS SNS para Notificaciones: Configuración y
          uso de AWS SNS para manejar notificaciones de IoT.
        </Text>
        <Text className="text-white text-white/90 mb-4">
          Hora 2: Construyendo un Tablero en Tiempo Real con React Introducción
          a React: Conceptos básicos de React y su papel en la construcción de
          aplicaciones web dinámicas. Conectando React a AWS: Uso del AWS
          Amplify y API Gateway para transmitir datos a una aplicación React.
          Ejercicio Práctico 3: Creando un tablero en tiempo real para
          visualizar datos de telemetría de IoT.{" "}
        </Text>
        <Text className="text-white font-bold mb-8 mt-2 text-xl">
          Público Objetivo
        </Text>
        <Text className="text-white text-white/90 mb-4">
          Desarrolladores y ingenieros de software Entusiastas y aficionados del
          IoT Profesionales de TI que buscan ampliar sus habilidades Estudiantes
          y educadores en campos relacionados con la tecnología
        </Text>

        <Text className="text-white font-bold mb-8 mt-2 text-xl">
          Requisitos Previos
        </Text>
        <Text className="text-white text-white/90 mb-4">
          Entendimiento básico de programación (Python, JavaScript/Node.js es
          una ventaja) Familiaridad con conceptos de desarrollo web
          Configuración de una cuenta de AWS (se proporcionarán instrucciones
          antes del taller)
        </Text>

        <Text className="text-white font-bold mb-8 mt-2 text-xl">
          Materiales del Taller
        </Text>
        <Text className="text-white text-white/90 mb-4">
          Folletos y documentación detallada Acceso a repositorios de código de
          ejemplo Lista de recursos útiles y lecturas adicionales
        </Text>
      </ScrollView>
    </Screen>
  );
}
