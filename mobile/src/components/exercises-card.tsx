import React, { useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

import LinearGradient from 'react-native-linear-gradient';
import Reanimated, {
  Easing,
  Extrapolation,
  interpolate,
  interpolateColor,
  useAnimatedProps,
  useAnimatedStyle,
  useDerivedValue,
  withTiming,
} from 'react-native-reanimated';
import styled from 'styled-components';

import { ArrowDownIcon, ArrowUp2Icon, EditIcon } from '@assets';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize, TPropsExercise } from '~types';

type TProps = {
  exercises: TPropsExercise;
  onEdit: () => void;
};

const AnimatedLinearGradient =
  Reanimated.createAnimatedComponent(LinearGradient);

export const ExercisesCard = ({ exercises, onEdit }: TProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isEndAnimation, setIsEndAnimation] = useState(true);
  const height = normVert(78);
  const count = exercises.exercises.length;
  const duration = 200 + 50 * count;

  const derived = useDerivedValue(
    () =>
      isOpen
        ? withTiming(1, { duration, easing: Easing.linear })
        : withTiming(0, { duration, easing: Easing.linear }),
    [isOpen],
  );

  const heightStyles = useAnimatedStyle(() => ({
    maxHeight: interpolate(derived.value, [0, 1], [height, 100 + 100 * count], {
      extrapolateRight: Extrapolation.CLAMP,
    }),
  }));

  const gradientProps = useAnimatedProps(() => ({
    colors: [
      interpolateColor(
        derived.value,
        [0, 1],
        ['rgba(255, 255, 255, 0.2)', colors.black3],
      ),
      interpolateColor(
        derived.value,
        [0, 1],
        ['rgba(255, 255, 255, 0.002)', colors.black3],
      ),
    ],
  }));

  const handleOpen = () => {
    setIsOpen(isOpen => !isOpen);

    if (isEndAnimation) {
      setIsEndAnimation(isEndAnimation => !isEndAnimation);
    } else {
      setTimeout(() => {
        setIsEndAnimation(isEndAnimation => !isEndAnimation);
      }, duration);
    }
  };

  return (
    <Reanimated.View style={[styles.box, heightStyles]}>
      <Container
        colors={[colors.black3, colors.black3]}
        animatedProps={gradientProps}
      >
        <View style={[!isEndAnimation && styles.topContainer, styles.row]}>
          <View>
            <View style={[styles.row, { justifyContent: 'flex-start' }]}>
              <Text color={colors.white} fontSize={FontSize.S17}>
                {exercises.name}
              </Text>
              <Icon onPress={onEdit}>
                <EditIcon fill={colors.green} />
              </Icon>
            </View>
            <Text
              style={styles.exercisesText}
              color={colors.black4}
              fontSize={FontSize.S12}
            >
              {exercises.exercises.length} {t('createPlan.exercises')}
            </Text>
          </View>
          {exercises.exercises.length ? (
            <Icon onPress={handleOpen}>
              {isOpen ? <ArrowUp2Icon /> : <ArrowDownIcon />}
            </Icon>
          ) : null}
        </View>
        {!isEndAnimation &&
          exercises.exercises?.map((exercise, key) => (
            <View key={key} style={[styles.exercise, styles.row]}>
              <Text fontSize={FontSize.S12} color={colors.white}>
                {key + 1}. {exercise.name}
              </Text>
              <View style={styles.row}>
                {exercise.sets.map((set, key) => (
                  <React.Fragment key={key}>
                    <Text fontSize={FontSize.S12} color={colors.white}>
                      {set}
                    </Text>
                    {key !== exercise.sets.length - 1 && (
                      <Text fontSize={FontSize.S12} color={colors.green}>
                        ,{' '}
                      </Text>
                    )}
                  </React.Fragment>
                ))}
              </View>
            </View>
          ))}
      </Container>
    </Reanimated.View>
  );
};

const styles = StyleSheet.create({
  box: { overflow: 'hidden', marginBottom: normVert(19), borderRadius: 12 },
  exercisesText: {
    marginTop: normVert(10),
  },
  topContainer: {
    borderBottomColor: colors.grey7,
    borderBottomWidth: 1,
    paddingBottom: normVert(16),
    marginBottom: normVert(4),
  },
  exercise: {
    marginTop: normVert(12),
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
});

const Container = styled(AnimatedLinearGradient)`
  width: 100%;
  padding-vertical: ${normVert(16)}px;
  padding-horizontal: ${normHor(16)}px;
`;

const Icon = styled(TouchableOpacity)`
  margin-left: ${normHor(13)}px;
`;
