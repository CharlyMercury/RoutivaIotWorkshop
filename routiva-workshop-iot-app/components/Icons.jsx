import { MaterialCommunityIcons } from "@expo/vector-icons";
import { AntDesign } from "@expo/vector-icons";

export const CircleInfoIcon = (props) => (
  <MaterialCommunityIcons
    name="information"
    size={34}
    color="white"
    {...props}
  />
);

export const HomeIcon = (props) => (
  <MaterialCommunityIcons
    name="home-automation"
    size={34}
    color="white"
    {...props}
  />
);

export const InfoIcon = (props) => (
  <MaterialCommunityIcons
    name="information-variant"
    size={34}
    color="white"
    {...props}
  />
);

export const FormIcon = (props) => (
  <AntDesign name="form" size={24} color="white" {...props} />
);
