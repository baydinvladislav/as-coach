import { action, computed, makeObservable, observable } from 'mobx';

import { login, me, registration } from '@api';
import { TOKEN } from '@constants';
import { storage } from '@utils';

import { RootStore } from './RootStore';
import { actionLoading } from './action-loading';

type UserProps = {
  username: string;
  phone: string;
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
    phone: '',
  };

  @action
  setHasAccess(isSignedIn: boolean) {
    this.isSignedIn = isSignedIn;
  }

  @computed get hasAccess() {
    return this.isSignedIn;
  }

  @actionLoading()
  @action
  async login({ phone, password }: { phone: string; password: string }) {
    try {
      const {
        data: { access_token },
      } = await login(phone, password);
      await new Promise(resolve =>
        setTimeout(() => {
          resolve({});
        }, 1000),
      );
      await storage.setItem(TOKEN, access_token);

      const { data } = await me();

      this.setHasAccess(true);
      this.me = data.me;
      return data.me;
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  async register({ username, password }: any) {
    try {
      const { data } = await registration(username, password);

      this.setHasAccess(true);
      this.me = data.me;
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  logout() {
    this.isSignedIn = false;
  }
}
