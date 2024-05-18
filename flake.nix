{
  description = "Python and Hatch with Nix";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [];
      systems = [ "x86_64-linux" ];
      perSystem = { config, self', inputs', pkgs, system, ... }: {
        #packages.default = pkgs.hello;
        devShells.default = pkgs.mkShell {
          name = "labyrinths-py-dev";
          packages = with pkgs; [
            # C++ Compiler is already part of stdenv
            hatch
          ];
        };
      };
      flake = {};
    };
}
