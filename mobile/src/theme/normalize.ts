import { Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');
const [shortDimension, longDimension] =
  width < height ? [width, height] : [height, width];

const guidelineBaseWidth = 375;
const guidelineBaseHeight = 812;

export const normHor = (size: number): number =>
  (shortDimension / guidelineBaseWidth) * size;
export const normVert = (size: number): number =>
  (longDimension / guidelineBaseHeight) * size;
