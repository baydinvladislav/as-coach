import React from 'react';

import { ExercisesCard } from '@components';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { ModalLayout, ViewWithButtons } from '@ui';

export const DetailPlanScreen = () => {
  const { navigate } = useNavigation();

  return (
    <ModalLayout>
      <ViewWithButtons
        style={{ justifyContent: 'space-between' }}
        onCancel={() => navigate(Screens.DetailClient)}
        onConfirm={() => navigate(Screens.DetailClient)}
        confirmText={t('buttons.add')}
      >
        <ExercisesCard
          onEdit={() => null}
          exercises={{
            name: 'Test',
            exercises: [
              {
                id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
                name: 'test',
                sets: [12, 12, 12],
              },
              {
                id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
                name: 'test',
                sets: [12, 12, 12],
              },
              {
                id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
                name: 'test',
                sets: [12, 12, 12],
              },
              {
                id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
                name: 'test',
                sets: [12, 12, 12],
              },
              {
                id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
                name: 'test',
                sets: [12, 12, 12],
              },
              {
                id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
                name: 'test',
                sets: [12, 12, 12],
              },
              {
                id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
                name: 'test',
                sets: [12, 12, 12],
              },
              {
                id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
                name: 'test',
                sets: [12, 12, 12],
              },
            ],
          }}
        />
        <ExercisesCard
          onEdit={() => null}
          exercises={{
            name: 'Test',
            exercises: [
              {
                id: '7ea243a7-356a-443e-ac44-697320be8f08',
                name: 'test',
                sets: [12, 12, 12],
              },
            ],
          }}
        />
        <ExercisesCard
          onEdit={() => null}
          exercises={{
            name: 'Test',
            exercises: [
              {
                id: '9b811d46-3efc-4ad2-8393-f2633014fa5d',
                name: 'test',
                sets: [12, 12, 12],
              },
            ],
          }}
        />
      </ViewWithButtons>
    </ModalLayout>
  );
};
