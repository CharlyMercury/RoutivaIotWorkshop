// App.js
import { Screen } from "../../components/Screen";
import React from "react";
import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator,
} from "react-native";
import axios from "axios";

const App = () => {
  const [formData, setFormData] = useState({ key1: "", key2: "", key3: "" });
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (key, value) => {
    setFormData({ ...formData, [key]: value });
  };

  const sendRequest = async () => {
    // Check for empty fields
    if (!formData.key1 || !formData.key2 || !formData.key3) {
      Alert.alert("Error", "No dejes ningún campo vacío.");
      return;
    }

    setLoading(true); // Show activity indicator

    try {
      const result = await axios.post(
        "https://y4bpify9tj.execute-api.us-east-1.amazonaws.com/Test/data-form",
        formData,
      );
      setResponse(result.data);
      Alert.alert("Éxito", "¡Información Enviada Correctamente!");
      setFormData({ key1: "", key2: "", key3: "" });
    } catch (error) {
      console.error("Error sending request:", error);
      Alert.alert("Error", "¡Información Enviada Incorrectamente!");
    } finally {
      setLoading(false); // Hide activity indicator
    }
  };

  return (
    <Screen>
      <ScrollView>
        <View className="w-full max-w-md">
          <Text className="text-white text-2xl font-bold text-center mb-6">
            Déjanos tus comentarios
          </Text>

          <View className="mb-4">
            <Text className="text-white text-lg mb-2"> Nombre </Text>
            <TextInput
              className="text-black border border-gray-300 rounded p-2 text-lg bg-white"
              placeholder="Carlos Tovar"
              placeholderTextColor="rgba(0, 0, 0, 0.2)"
              value={formData.key1}
              onChangeText={(value) => handleInputChange("key1", value)}
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
              placeholderTextColor="rgba(0, 0, 0, 0.2)"
              keyboardType="email-address"
              value={formData.key2}
              onChangeText={(value) => handleInputChange("key2", value)}
            />
          </View>

          <View className="mb-4">
            <Text className="text-white text-lg mb-2">Description</Text>
            <TextInput
              className="text-black border border-gray-300 rounded p-2 text-lg bg-white h-32"
              placeholder=" Describe tu experiencia y comentarios sobre el curso"
              placeholderTextColor="rgba(0, 0, 0, 0.2)"
              multiline
              numberOfLines={4}
              value={formData.key3}
              onChangeText={(value) => handleInputChange("key3", value)}
            />
          </View>

          <TouchableOpacity
            className="bg-blue-500 rounded p-2 items-center mt-2"
            onPress={sendRequest}
          >
            {response && <Text></Text>}
            <Text className="text-white text-lg font-semibold">
              {""}
              Enviar reseña{""}
            </Text>
          </TouchableOpacity>

          {loading && (
            <View className="flex items-center justify-center mt-4">
              <ActivityIndicator size="large" />
            </View>
          )}
        </View>
      </ScrollView>
    </Screen>
  );
};

export default App;
