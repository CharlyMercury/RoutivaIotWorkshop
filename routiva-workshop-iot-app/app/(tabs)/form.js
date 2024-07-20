// App.js
import { Screen } from "../../components/Screen";
import React from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
} from "react-native";

const App = () => {
  return (
    <Screen>
      <ScrollView>
        <View className="w-full max-w-md">
          <Text className="text-white text-2xl font-bold text-center mb-6">
            Sign Up
          </Text>

          <View className="mb-4">
            <Text className="text-white text-lg mb-2"> Nombre </Text>
            <TextInput
              className="text-black border border-gray-300 rounded p-2 text-lg bg-white"
              placeholder="Carlos Tovar"
            />
          </View>

          <View className="mb-4">
            <Text className="text-white text-lg mb-2">
              {" "}
              Correo Electrónico{" "}
            </Text>
            <TextInput
              className="text-black border border-gray-300 rounded p-2 text-lg bg-white"
              placeholder="ejemplo@gmail.com"
              keyboardType="email-address"
            />
          </View>

          <View className="mb-4">
            <Text className="text-white text-lg mb-2">Description</Text>
            <TextInput
              className="text-black border border-gray-300 rounded p-2 text-lg bg-white h-32"
              placeholder=" Describe tu experiencia y comentarios sobre el curso"
              multiline
              numberOfLines={4}
            />
          </View>

          <TouchableOpacity
            className="bg-blue-500 rounded p-3 items-center mt-4"
            onPress={() => alert("Form Submitted")}
          >
            <Text className="text-white text-lg font-semibold">
              {" "}
              Enviar reseña{" "}
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </Screen>
  );
};

export default App;
