import { ActivityIndicator, Image, ScrollView, Text, View } from "react-native";
import { Link, useLocalSearchParams, Stack } from "expo-router";
import { useState, useEffect } from "react";
import { Screen } from "../components/Screen";
import { getIotsDetails } from "../lib/iot";

export default function Detail() {
  const { iotlocation } = useLocalSearchParams();

  const [iots, setIots] = useState([]);

  useEffect(() => {
    if (iotlocation) {
      getIotsDetails(iotlocation).then(setIots);
    }
  }, [iotlocation]);

  return (
    <Screen>
      <Stack.Screen
        options={{
          headerStyle: { backgroundColor: "white " },
          headerTintColor: "black",
          headerLeft: () => {},
          headerTitle: iots.title,
          headerRight: () => {},
        }}
      />
      <View>
        <ScrollView>
          <View className="justify-center items-center text-center">
            <Image
              className="mb-4 rounded"
              source={{ uri: iots.image }}
              style={{ width: 214, height: 294 }}
            />
            <Text className="text-white text-center font-bold text-xl">
              {iots.title}
            </Text>
            <Text className="text-white/70 mt-4 text-left mb-8 text-base">
              {iots.description}
            </Text>
          </View>
        </ScrollView>
      </View>
    </Screen>
  );
}
