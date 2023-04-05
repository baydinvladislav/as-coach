import { action, computed, makeObservable, observable } from 'mobx';

import { login, me, profileEdit, registration } from '@api';
import { TOKEN } from '@constants';
import { storage } from '@utils';

import { RootStore } from './RootStore';
import { actionLoading } from './action-loading';

type UserProps = {
  first_name: string;
  last_name: string;
  username: string;
  password: string;
  gender: string;
  birthday: string;
  email: string;
};

export default class UserStore {
  rootStore: RootStore;

  constructor(root: RootStore) {
    this.rootStore = root;
    makeObservable(this);
  }

  @observable isSignedIn = false;
  @observable me: UserProps = {
    first_name: '',
    last_name: '',
    username: '',
    password: '',
    gender: '',
    birthday: '',
    email: '',
  };

  @action
  setHasAccess(isSignedIn: boolean) {
    this.isSignedIn = isSignedIn;
  }

  @computed get hasAccess() {
    return this.isSignedIn;
  }

  @action
  @actionLoading()
  async login(values: { username: string; password: string }) {
    try {
      const {
        data: { access_token },
      } = await login(values);

      await storage.setItem(TOKEN, access_token ?? '');

      this.setHasAccess(true);

      const { data } = await me();

      this.me = data;
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  @actionLoading()
  async register(values: {
    first_name: string;
    username: string;
    password: string;
  }) {
    try {
      await registration(values);
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  @actionLoading()
  async profileEdit(values: {
    first_name?: string;
    last_name?: string;
    username?: string;
    password?: string;
    gender?: string;
    birthday?: string;
    email?: string;
  }) {
    try {
      const { data } = await profileEdit(values);
      this.me = data;
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
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }
}
