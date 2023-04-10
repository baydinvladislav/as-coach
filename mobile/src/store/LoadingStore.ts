import {
  action,
  computed,
  makeAutoObservable,
  makeObservable,
  observable,
} from 'mobx';

export class LoadingStore {
  @observable loadingStatus = 0;

  constructor() {
    makeObservable(this);
  }

  @computed
  get isLoading(): boolean {
    return !!this.loadingStatus;
  }

  @action
  increaseLoadingStatus() {
    this.loadingStatus = this.loadingStatus + 1;
  }

  @action
  decreaseLoadingStatus() {
    this.loadingStatus = this.loadingStatus - 1;
  }
}
