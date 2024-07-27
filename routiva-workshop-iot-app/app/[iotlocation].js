import { Image, Pressable, ScrollView, Text, View } from "react-native";
import { useLocalSearchParams, Stack } from "expo-router";
import { useState, useEffect } from "react";
import { Screen } from "../components/Screen";
import { getIotsDetails } from "../lib/iot";

import awsmobile from "../lib/aws-export";
import { Amplify } from "aws-amplify";
import { PubSub } from "@aws-amplify/pubsub";
import { FanIcon, LightBulbIcon } from "../components/Icons";

import { PermissionsAndroid } from "react-native";
PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS);

Amplify.configure(awsmobile);

const pubsub = new PubSub({
  endpoint: "wss://a1svajesngnqg2-ats.iot.us-east-1.amazonaws.com/mqtt",
  region: "us-east-1",
});

export default function Detail() {
  const [isActive, setIsActive] = useState(false);
  const [actuator, setActuator] = useState("");
  const [isFanActive, setIsFanActive] = useState(false);
  let state = false;

  const handlePress = () => {
    setIsActive(!isActive);
    setActuator("leds");
  };

  const handleFanPress = () => {
    setIsFanActive(!isFanActive);
    setActuator("fans");
  };

  const { iotlocation } = useLocalSearchParams();

  const [iots, setIots] = useState([]);

  useEffect(() => {
    if (iotlocation) {
      getIotsDetails(iotlocation).then(setIots);
    }
  }, [iotlocation]);

  useEffect(() => {
    pubsub.subscribe({ topics: [] }).subscribe({});
  }, [iotlocation]);

  useEffect(() => {
    pubsub
      .publish({
        topics: "actuator",
        message: {
          action: {
            "turn-on": actuator,
            location: iotlocation,
            state: actuator === "leds" ? isActive : isFanActive,
          },
        },
        qos: 1,
      })
      .catch((err) => console.error(err));
  }, [actuator, iotlocation, isActive, isFanActive, setIsActive]);

  return (
    <Screen>
      <Stack.Screen
        options={{
          headerStyle: { backgroundColor: "#448aff" },
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
          <View>
            <Pressable onPress={handlePress}>
              <LightBulbIcon
                className="justify-center items-center text-center"
                color={isActive ? "yellow" : "gray"}
              />
              <Text className="text-white text-center font-bold text-xl">
                {isActive ? "Encendido" : "Apagado"}
              </Text>
            </Pressable>
            {iots.actuator ? (
              <Pressable onPress={handleFanPress}>
                <FanIcon
                  className="mt-4 justify-center items-center text-center mb"
                  color={isFanActive ? "yellow" : "gray"}
                />
                <Text className="text-white text-center font-bold text-xl">
                  {isFanActive ? "Encendido" : "Apagado"}
                </Text>
              </Pressable>
            ) : (
              ""
            )}
          </View>
        </ScrollView>
      </View>
    </Screen>
  );
}
