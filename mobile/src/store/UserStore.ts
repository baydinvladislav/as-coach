import { action, computed, makeObservable, observable } from 'mobx';

import {
  changePassword,
  confirmPassword,
  login,
  me,
  profileEdit,
  registration,
} from '@api';
import { TOKEN } from '@constants';
import { storage } from '@utils';

import { UserType } from '~types';

import { RootStore } from './RootStore';
import { actionLoading } from './action-loading';

export type UserProps = {
  id: string;
  first_name: string;
  last_name: string;
  username: string;
  password: string;
  gender: string;
  birthday: string;
  email: string;
  user_type: UserType | null;
  photo_link: string | null;
  photo: {
    name?: string;
    type?: string;
    uri?: string;
  };
};

export default class UserStore {
  rootStore: RootStore;

  constructor(root: RootStore) {
    this.rootStore = root;
    makeObservable(this);
  }

  @observable isSignedIn = false;
  @observable me: UserProps = {
    id: '',
    user_type: null,
    first_name: '',
    last_name: '',
    username: '',
    password: '',
    gender: '',
    birthday: '',
    email: '',
    photo_link: null,
    photo: {},
  };

  @action
  setHasAccess(isSignedIn: boolean) {
    this.isSignedIn = isSignedIn;
  }

  @action
  setMe(me: Partial<UserProps>) {
    this.me = me as UserProps;
  }

  @computed get hasAccess() {
    return this.isSignedIn;
  }

  @action
  async getMe() {
    try {
      const { data } = await me();
      this.setHasAccess(true);
      this.setMe({ ...data });
    } catch (e) {
      console.warn(e);
    }
  }

  @action
  @actionLoading()
  async login(values: Partial<UserProps>) {
    try {
      const {
        data: { access_token },
      } = await login(values);

      await storage.setItem(TOKEN, access_token ?? '');

      this.setHasAccess(true);
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  @actionLoading()
  async register(values: Partial<UserProps>) {
    try {
      const {
        data: { access_token },
      } = await registration(values);

      await storage.setItem(TOKEN, access_token ?? '');

      this.setHasAccess(true);
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  @actionLoading()
  async profileEdit(values: Partial<UserProps>) {
    try {
      const { data } = await profileEdit(values);
      this.setMe(data);
    } catch (e) {
      console.warn(JSON.stringify(e));
      throw e;
    }
  }

  @action
  @actionLoading()
  async confirmPassword(values: Pick<UserProps, 'password'>) {
    try {
      const { data } = await confirmPassword(values);
      return data;
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  @actionLoading()
  async changePassword(values: Pick<UserProps, 'password'>) {
    try {
      const { data } = await changePassword(values);
      return data;
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  async logout() {
    try {
      storage.removeItem(TOKEN);
      this.isSignedIn = false;
      this.setMe({});
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }
}
