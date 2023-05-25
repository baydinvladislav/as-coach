import { PlanScreens } from '@screens';
import { CustomerProps } from '@store';

export enum FontWeight {
  'Regular' = 'Ubuntu Regular',
  'Medium' = 'Ubuntu Medium',
  'Bold' = 'Ubuntu Bold',
}
export enum FontSize {
  'S24' = '24px',
  'S20' = '20px',
  'S17' = '17px',
  'S16' = '16px',
  'S12' = '12px',
  'S10' = '10px',
}

export enum ButtonType {
  PRIMARY = 'primary',
  SECONDARY = 'secondary',
  TEXT = 'text',
}

export enum UserType {
  COACH = 'coach',
  CLIENT = 'client',
}

export enum ExerciseCardType {
  SIMPLE = 'simple',
  FULL = 'full',
}

export type TResponseError = {
  loc?: string[];
  msg: string;
  type: string;
}[];

export type TResponseConfirmPassword = {
  confirmed_password: boolean;
};

export type TPlan = {
  diets: { proteins: string; fats: string; carbs: string }[];
  start_date: string;
  end_date: string;
  trainings: TPropsExercise[];
  notes: string;
  set_rest: string;
  exercise_rest: string;
  different_time: boolean;
};

export type TExercises = {
  id: string;
  muscle_group: string;
  name: string;
};

export type TExercisesEdited = {
  [key: string]: TExercises[];
};

export type TPropsExercise = {
  name: string;
  exercises: TPropsExercises[];
};

export type TPropsExercises = {
  id: string;
  name?: string;
  sets: number[];
  supersets?: string[];
  supersetId?: string;
};

export type TPlanType = {
  carbs: string;
  end_date: string;
  fats: string;
  id: string;
  trainings: TPropsExercise[];
  proteins: string;
  start_date: string;
  set_rest: number;
  exercise_rest: number;
  notes: string;
};

export type TFormProps = {
  customer: CustomerProps;
  clearErrors: () => void;
  errors: Record<string, any>;
  params: Record<string, any>;
  values: TPlan;
  handleSubmit: () => void;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate?: boolean,
  ) => void;
  setValues: React.Dispatch<React.SetStateAction<TPlan>>;
  isLoading: boolean;
};
