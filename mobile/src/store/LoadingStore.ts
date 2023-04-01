import {
  action,
  computed,
  makeAutoObservable,
  makeObservable,
  observable,
} from 'mobx';

export class LoadingStore {
  @observable loadingStatus = false;

  constructor() {
    makeObservable(this);
  }

  @computed
  get isLoading(): boolean {
    return this.loadingStatus;
  }

  @action
  increaseLoadingStatus() {
    this.loadingStatus = true;
  }

  @action
  decreaseLoadingStatus() {
    this.loadingStatus = false;
  }
}
