# temp-repo-name
TODO: {Simple overview goes here}

## Description

TODO: {Description of the project goes here}

## Getting Started


### Dependencies
- npm

### Installation
Clone this repository and run the following command from the root directory

``` shell
  $ npm install 
```

### Developing on this Repository

- Development: 
  
  Running the following command will watch changes to `src` folder and automatically sync to your local `dist` folder. 
  ``` shell
    $ npm run dev 
  ```
- Production: 
  ``` shell
    $ npm run production
  ```

- Chrome Extension:
  - Navigate to `chrome://extensions/` and turn on "Developer Mode"
  - Click on "Load unpacked" and choose `dist` folder
    - The extension should now be available as developer mode

- For UI work
  - Copy Chrome extension ID
    <div>
      <img src="https://user-images.githubusercontent.com/17207771/178127434-e1601546-fb6c-4d88-8ec9-462c0abf76e3.png" width=30% height=30% /> 
    </div>
    

  - Navigate to `chrome-extension://{EXTENSION_ID}/popup.html`
    

## Authors

| Name          | Email                | Github        |
| ------------- | -------------------- | ------------- |
| Sungho Cho    | sungh5c@gmail.com    | [link](https://github.com/sungho-cho)
| Jun Hur       | junhurcmu@gmail.com  | [link](https://github.com/junhur)
| Hyukjae Kwark | hkwark.ai@gmail.com  | [link](https://github.com/chorongi)

## Resources

- [Chrome Extension](https://developer.chrome.com/docs/extensions/)
- [Webpack](https://webpack.js.org/)
- [Babel](https://babeljs.io/)
- [React](https://reactjs.org/)
- [Typescript](https://www.typescriptlang.org/)