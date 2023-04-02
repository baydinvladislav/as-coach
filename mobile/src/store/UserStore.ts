import { action, computed, makeObservable, observable } from 'mobx';

import { login, me, registration } from '@api';
import { TOKEN } from '@constants';
import { storage } from '@utils';

import { RootStore } from './RootStore';
import { actionLoading } from './action-loading';

type UserProps = {
  username: string;
};

export default class UserStore {
  rootStore: RootStore;

  constructor(root: RootStore) {
    this.rootStore = root;
    makeObservable(this);
  }

  @observable isSignedIn = true;
  @observable me: UserProps = {
    username: '',
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
  async login({ phone, password }: { phone: string; password: string }) {
    try {
      await new Promise(resolve =>
        setTimeout(() => {
          resolve({});
        }, 1000),
      );
      const {
        data: { access_token },
      } = await login(phone, password);
      await storage.setItem(TOKEN, access_token);

      const { data } = await me();

      this.setHasAccess(true);
      this.me = data;
      return data.me;
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  @actionLoading()
  async register({
    username,
    phone,
    password,
  }: {
    username: string;
    phone: string;
    password: string;
  }) {
    try {
      await new Promise(resolve =>
        setTimeout(() => {
          resolve({});
        }, 1000),
      );
      const { data } = await registration(phone, username, password);

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
    } catch (e) {
      console.warn(e);
    }
  }
}
