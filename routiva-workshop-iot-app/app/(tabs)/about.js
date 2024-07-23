import { Screen } from "../../components/Screen";
import { ScrollView, Text, View } from "react-native";
import { FirebasePush } from "../../components/FirebasePush";

export default function About() {
  return (
    <View>
      <ScrollView>
        <Text className="text-white font-bold mb-8 text-2xl">
          Sobre el proyecto
        </Text>

        <Text className="text-white text-white/90 mb-4">
          lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea
        </Text>
        <FirebasePush />
      </ScrollView>
    </View>
  );
}
