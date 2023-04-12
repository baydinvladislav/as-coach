import React from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';
import styled from 'styled-components';

import { AddIcon } from '@assets';
import { CreatePlanItem } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import {
  Button,
  Checkbox,
  Input,
  InputSpinner,
  Keyboard,
  Text,
  ViewWithButtons,
} from '@ui';
import { isIOS } from '@utils';

import { ButtonType, FontSize } from '~types';

type TProps = {
  onNext: () => void;
  onPrev: () => void;
};

export const CreatePlanScreen = observer(({ onNext, onPrev }: TProps) => {
  const { loading } = useStore();

  const isDisabled = loading.isLoading;

  return (
    <Keyboard style={{ flex: 1, paddingTop: isIOS ? TOP_PADDING : 0 }}>
      {isIOS && (
        <TopBackground>
          <Line />
        </TopBackground>
      )}
      <Background style={{ flex: 1, paddingTop: isIOS ? 0 : TOP_PADDING }}>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={onPrev}
          onConfirm={() => console.log(123)}
          confirmText={t('buttons.next')}
          cancelText={t('buttons.prev')}
          isDisabled={isDisabled}
          isScroll={true}
        >
          <>
            <NameText>Сухарева София</NameText>
            <Text
              style={styles.title}
              color={colors.white}
              fontSize={FontSize.S24}
            >
              14 АВГ — 26 АВГ
            </Text>
            <CreatePlanItem title={t('createPlan.title1')}>
              <Checkbox
                style={styles.checkbox}
                placeholder={t('createPlan.checkboxDescription')}
              />
              <InputSpinner
                style={styles.input}
                placeholder={t('createPlan.placeholder1')}
              />
              <InputSpinner
                style={styles.input}
                placeholder={t('createPlan.placeholder2')}
              />
              <InputSpinner placeholder={t('createPlan.placeholder3')} />
            </CreatePlanItem>
            <CreatePlanItem title={t('createPlan.title2')}>
              <Button
                style={styles.addDayButton}
                type={ButtonType.TEXT}
                onPress={() => console.log(123)}
                leftIcon={<AddIcon stroke={colors.green} />}
              >
                {t('buttons.addDay')}
              </Button>
              <InputSpinner
                value={'0'}
                style={styles.input}
                placeholder={t('createPlan.description1')}
              />
              <InputSpinner
                value={'0'}
                style={styles.input}
                placeholder={t('createPlan.description2')}
              />
            </CreatePlanItem>
            <CreatePlanItem title={t('createPlan.title3')}>
              <Input
                placeholder={t('createPlan.enterText')}
                isTextarea={true}
                height={normVert(96)}
              />
            </CreatePlanItem>
          </>
        </ViewWithButtons>
      </Background>
    </Keyboard>
  );
});

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(14),
  },
  input: {
    marginBottom: normVert(20),
  },
  addDayButton: { marginRight: 'auto', marginBottom: normVert(20) },
  checkbox: {
    marginBottom: normVert(20),
  },
});

const NameText = styled(Text)`
  text-transform: uppercase;
  color: ${colors.black4};
  font-size: ${FontSize.S10};
  margin-bottom: ${normVert(16)}px;
`;

const Background = styled(View)`
  background-color: ${colors.black6};
  flex: 1;
  padding-top: ${normVert(40)}px;
`;

const TopBackground = styled(View)`
  background-color: ${colors.black6};
  flex: 1;
  position: absolute;
  top: ${normVert(34)}px;
  width: 100%;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  justify-content: center;
  align-items: center;
`;

const Line = styled(View)`
  background-color: ${colors.grey3};
  width: ${normHor(76)}px;
  height: ${normVert(6)}px;
  border-radius: 100px;
  margin-vertical: ${normVert(10)}px;
`;