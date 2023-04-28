import { axiosBase } from '@api';

import { TMuscleGroups } from '~types';

export const getMuscleGroups = () =>
  axiosBase.get<TMuscleGroups[]>('/muscle_groups');
