import { Link } from "expo-router";
import { useEffect, useRef } from "react";
import { View, Text, Image, Animated, Pressable } from "react-native";

export function IotCard({ iot }) {
  return (
    <Link href={`/${iot.slug}`} asChild>
      <Pressable className="active:opacity-70 border border-black active:border-white/50 bg-slate-500/10 p-4 rounded-xl">
        <View className="flex-row gap-4 mb-4" key={iot.slug}>
          <Image
            source={{ uri: iot.image }}
            className="mb-1 rounded-2xl w-36 h-36"
          />
          <View className="flex-shrink">
            <Text className="mt-3 text-slate-50 text-xl font-bold">
              {iot.title}
            </Text>
            <Text className="flex-shrink mt-3 text-sky-300 text-base">
              {iot.description}
            </Text>
          </View>
        </View>
      </Pressable>
    </Link>
  );
}

export function AnimatedIotCard({ iot, index }) {
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(opacity, {
      toValue: 1,
      duration: 500,
      delay: index * 250,
      useNativeDriver: true,
    }).start();
  }, [opacity, index]);

  return (
    <Animated.View style={{ opacity }}>
      <IotCard iot={iot} />
    </Animated.View>
  );
}
